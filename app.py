import os
import re
from http import HTTPStatus
from typing import Any

import requests
from dotenv import load_dotenv
from flask import Flask, Response, make_response, redirect, render_template, request

load_dotenv()

app = Flask(__name__, static_folder="public", static_url_path="")
app.secret_key = os.getenv("SECRET_KEY", "change-me-in-production")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080").rstrip("/")
REQUEST_TIMEOUT = int(os.getenv("BACKEND_TIMEOUT", "15"))
SERVER_NAME = "OsuZenith"
HOME_FALLBACK_DESCRIPTION = "A relax server for clean plays, player profiles, leaderboards, and fast access to the latest build."
HOME_FALLBACK_CHANGELOG = "No server updates published yet."
BRAND_REPLACEMENTS = {
    "osudroid!relax": SERVER_NAME,
    "osu!droid": SERVER_NAME,
    "osu!zenith": SERVER_NAME,
    "Classic Dark Portal": SERVER_NAME,
}
DESIGN_COPY_MARKERS = (
    "cupertino",
    "graphite surfaces",
    "layered reflections",
    "restrained blue highlights",
    "classic depth",
    "fluid motion",
    "ambient drift",
    "light sweeps",
    "safer links",
    "placeholder urls",
    "premium feel",
    "theme",
)


def env_value(*names: str) -> str | None:
    """Return the first non-empty environment variable from a list of possible names."""
    for name in names:
        value = os.getenv(name)
        if value and value.strip():
            return value.strip()
    return None


def first_value(*values: Any) -> Any:
    """Return the first non-empty value, preserving non-string values like 0."""
    for value in values:
        if isinstance(value, str):
            if value.strip():
                return value.strip()
        elif value not in (None, ""):
            return value
    return None


def site_value(site: dict, *keys: str) -> Any:
    for key in keys:
        value = site.get(key)
        if value not in (None, ""):
            return value
    return None


def backend_url(path: str) -> str:
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{BACKEND_URL}{path}"


def brand_text(raw: Any) -> str:
    text = str(raw or "")
    for old, new in BRAND_REPLACEMENTS.items():
        text = re.sub(re.escape(old), new, text, flags=re.IGNORECASE)
    return text.strip()


def home_text(raw: Any, fallback: str) -> str:
    text = brand_text(raw)
    if not text:
        return fallback
    lowered = text.lower()
    if any(marker in lowered for marker in DESIGN_COPY_MARKERS):
        return fallback
    return text


def safe_external_link(raw: str | None) -> str | None:
    if not raw:
        return None
    link = raw.strip()
    unsafe_values = {"#", "about:blank", "javascript:void(0)", "javascript:;"}
    if not link or link.lower() in unsafe_values:
        return None
    if "placeholder" in link.lower() or "example.com" in link.lower():
        return None
    if not (link.startswith("http://") or link.startswith("https://") or link.startswith("/")):
        return None
    return link


def api_response(resp: requests.Response) -> tuple[Any, str | None, int]:
    try:
        body = resp.json()
    except ValueError:
        return None, resp.text or "Backend returned an invalid response", resp.status_code

    status = body.get("status")
    data = body.get("data")
    if resp.ok and status == "success":
        return data, None, resp.status_code
    return None, str(data or status or "Backend error"), resp.status_code


def api_get(path: str, params: dict | None = None) -> tuple[Any, str | None, int]:
    try:
        resp = requests.get(backend_url(path), params=params, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        return None, f"Could not reach backend: {exc}", HTTPStatus.BAD_GATEWAY
    return api_response(resp)


def api_post(path: str, data: dict | None = None, files: dict | None = None) -> tuple[Any, str | None, int]:
    try:
        resp = requests.post(backend_url(path), data=data, files=files, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        return None, f"Could not reach backend: {exc}", HTTPStatus.BAD_GATEWAY
    return api_response(resp)


@app.route("/user/avatar/<int:uid>.png")
def user_avatar(uid: int):
    try:
        resp = requests.get(
            backend_url(f"/api/assets/avatar/{uid}.png"),
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException:
        return Response(status=HTTPStatus.BAD_GATEWAY, mimetype="image/png")

    headers = {}
    cache_control = resp.headers.get("Cache-Control")
    if cache_control:
        headers["Cache-Control"] = cache_control

    return Response(
        resp.content,
        status=resp.status_code,
        headers=headers,
        mimetype=resp.headers.get("Content-Type", "image/png"),
    )


def current_login_state() -> str | None:
    return request.cookies.get("login_state")


def player_id_from_cookie() -> int | None:
    raw = current_login_state()
    if not raw:
        return None
    try:
        return int(raw.split("-")[1])
    except (ValueError, IndexError):
        return None


def render_error(message: str):
    return render_template("error.jinja", error_message=message)


def render_success(message: str):
    return render_template("success.jinja", success_message=message)


def level_from_ranked_score(rscore: int) -> int:
    def level_formula(i: int) -> int:
        if i >= 100:
            return 26931190827 + 99999999999 * (i - 100)
        return int((5000 / 3 * (4 * i**3 - 3 * i**2 - i)) + 1.25 ** (i - 60))

    i = 1
    while i < 1000:
        cur = level_formula(i)
        nxt = level_formula(i + 1)
        if cur <= rscore <= nxt:
            return i
        if cur > rscore and nxt > rscore:
            return i
        i += 1
    return 1000


def beatmap_name(bmap: dict | None) -> str:
    if not bmap:
        return "Unknown beatmap"
    return f"{bmap.get('artist', '')} - {bmap.get('title', '')} [{bmap.get('version', '')}]".strip()


def normalize_score(score: dict) -> dict:
    bmap = score.get("bmap") or {}
    bmap["full"] = beatmap_name(bmap)
    score["bmap"] = bmap
    score["link"] = f"https://osu.ppy.sh/b/{bmap.get('id')}" if bmap.get("id") else "#"
    score["mods_display"] = score.get("mods") or "NM"
    try:
        score["pp_display"] = round(float(score.get("pp") or 0), 2)
    except (TypeError, ValueError):
        score["pp_display"] = 0
    return score


@app.route("/")
def index():
    site, error, _ = api_get("/api/frontend/site")
    if error or not isinstance(site, dict):
        # The landing page should still load when the backend site endpoint is not
        # available, because deploy-time variables such as CLIENT_DOWNLOAD_URL,
        # DISCORD_URL, GITHUB_URL and CLIENT_VERSION live in the frontend app.
        site = {}

    download_link = safe_external_link(
        first_value(
            env_value("CLIENT_DOWNLOAD_URL", "DOWNLOAD_URL"),
            site_value(site, "download_link", "download_url", "client_download_url"),
        )
    )
    discord_url = safe_external_link(
        first_value(
            env_value("DISCORD_URL", "DISCORD_INVITE_URL"),
            site_value(site, "discord_url", "discord", "discord_invite_url"),
        )
    )
    github_url = safe_external_link(
        first_value(
            env_value("GITHUB_URL", "GITHUB_REPOSITORY_URL"),
            site_value(site, "github_url", "github", "repository_url"),
        )
    )
    version = (
        first_value(
            env_value("CLIENT_VERSION", "VERSION"),
            site_value(site, "version", "client_version"),
            "0",
        )
        or "0"
    )

    return render_template(
        "main_page.jinja",
        players=site.get("players", 0),
        online=site.get("online", 0),
        title=SERVER_NAME,
        description=home_text(site_value(site, "description", "server_description"), HOME_FALLBACK_DESCRIPTION),
        changelog=home_text(site_value(site, "changelog", "updates"), HOME_FALLBACK_CHANGELOG),
        download_link=download_link,
        discord_url=discord_url,
        github_url=github_url,
        version=str(version).strip() or "0",
    )


@app.route("/user/leaderboard")
def leaderboard():
    sortby = request.args.get("sortby", "pp").lower()
    if sortby not in {"pp", "score"}:
        sortby = "pp"
    country = (request.args.get("country") or "").upper() or None

    lb_data, error, _ = api_get("/api/leaderboard", {"type": sortby, "country": country} if country else {"type": sortby})
    if error:
        return render_error(error), 502

    countries, countries_error, _ = api_get("/api/get_countries")
    if countries_error:
        countries = []

    leaderboard_rows = []
    for player in lb_data or []:
        stats = player.get("stats") or {}
        leaderboard_rows.append(
            {
                "id": player.get("id"),
                "username": player.get("username", ""),
                "pp_rank": stats.get("pp_rank", 0),
                "score_rank": stats.get("score_rank", 0),
                "country_pp_rank": stats.get("country_pp_rank", 0),
                "country_score_rank": stats.get("country_score_rank", 0),
                "pp": round(float(stats.get("pp") or 0), 2),
                "rscore": f"{int(stats.get('rscore') or 0):,}",
                "plays": stats.get("plays", 0),
            }
        )

    return render_template(
        "leaderboard.jinja",
        leaderboard=leaderboard_rows,
        country=country,
        countries=countries or [],
        sortby=sortby,
    )


@app.route("/user/profile.php")
def profile():
    player_id = request.args.get("id") or request.args.get("uid") or player_id_from_cookie()
    if not player_id:
        return render_error("No player ID provided"), 400

    player, error, status = api_get("/api/get_user", {"id": player_id})
    if error:
        return render_error(error), status

    recent_scores, _, _ = api_get("/api/get_scores", {"id": player_id, "limit": 50})
    top_scores, _, _ = api_get("/api/top_scores", {"id": player_id, "limit": 50})
    recent_scores = [normalize_score(score) for score in (recent_scores or [])]
    top_scores = [normalize_score(score) for score in (top_scores or [])]

    player_stats = dict(player.get("stats") or {})
    rscore_int = int(player_stats.get("rscore") or 0)
    level = level_from_ranked_score(rscore_int)
    player_stats["acc"] = f"{float(player_stats.get('acc') or 0):.2f}%"
    player_stats["rscore"] = f"{rscore_int:,}"

    return render_template(
        "profile.jinja",
        player_stats=player_stats,
        recent_scores=recent_scores,
        top_scores=top_scores,
        player=player,
        level=level,
        avatar_url=f"/user/avatar/{player_id}.png",
    )


@app.route("/user/web_login.php", methods=["GET", "POST"])
def web_login():
    if current_login_state():
        return render_error("Already logged in")

    if request.method == "POST":
        data, error, status = api_post(
            "/api/frontend/auth/login",
            {"username": request.form.get("username"), "password": request.form.get("password")},
        )
        if error:
            return render_template("web_login.jinja", error_message=error), status

        response = make_response(redirect(f"/user/profile.php?id={data['player']['id']}"))
        response.set_cookie("login_state", data["login_state"], max_age=60 * 60 * 24 * 365, httponly=True, samesite="Lax")
        return response

    return render_template("web_login.jinja")


@app.route("/user/logout.php")
def logout():
    response = make_response(render_success("Logout successful"))
    response.delete_cookie("login_state")
    return response


@app.route("/api/register.php", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data, error, status = api_post(
            "/api/frontend/auth/register",
            {
                "username": request.form.get("username"),
                "password": request.form.get("password"),
                "email": request.form.get("email"),
            },
        )
        if error:
            return render_error(error), status
        response = make_response(redirect(f"/user/profile.php?id={data['player']['id']}"))
        response.set_cookie("login_state", data["login_state"], max_age=60 * 60 * 24 * 365, httponly=True, samesite="Lax")
        return response
    return render_template("register.jinja")


@app.route("/user/account/settings")
def account_settings():
    if not current_login_state():
        return render_error("Not logged in"), 401
    return render_template("account/settings.jinja")


@app.route("/user/account/change-password", methods=["POST"])
def account_change_password():
    data, error, status = api_post(
        "/api/frontend/account/change-password",
        {
            "login_state": current_login_state(),
            "old_password": request.form.get("old_password"),
            "new_password": request.form.get("new_password"),
            "confirm_password": request.form.get("confirm_password"),
        },
    )
    return (render_error(error), status) if error else render_success(data.get("message", "Password changed"))


@app.route("/user/account/change-username", methods=["POST"])
def account_change_username():
    data, error, status = api_post(
        "/api/frontend/account/change-username",
        {"login_state": current_login_state(), "new_username": request.form.get("new_username")},
    )
    if error:
        return render_error(error), status
    response = make_response(render_success(data.get("message", "Username changed")))
    if data.get("login_state"):
        response.set_cookie("login_state", data["login_state"], max_age=60 * 60 * 24 * 365, httponly=True, samesite="Lax")
    return response


@app.route("/user/account/change-email", methods=["POST"])
def account_change_email():
    data, error, status = api_post(
        "/api/frontend/account/change-email",
        {"login_state": current_login_state(), "new_email": request.form.get("new_email")},
    )
    return (render_error(error), status) if error else render_success(data.get("message", "Email changed"))


@app.route("/user/account/set-avatar", methods=["POST"])
def account_set_avatar():
    uploaded = request.files.get("avatar")
    if not uploaded:
        return render_error("No avatar file provided"), 400
    files = {"avatar": (uploaded.filename, uploaded.stream, uploaded.mimetype)}
    data, error, status = api_post(
        "/api/frontend/account/set-avatar",
        {"login_state": current_login_state()},
        files=files,
    )
    return (render_error(error), status) if error else render_success(data.get("message", "Avatar uploaded"))


@app.route("/user/password_recovery", methods=["GET", "POST"])
def password_recovery():
    return render_error("Password recovery is not implemented in the separated frontend yet."), 501
