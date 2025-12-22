import logging
import os
import hashlib
import discord_webhook
import uuid
import geoip2.database
import aiohttp
from objects import glob


def make_safe(n: str):
    return n.lower().replace(" ", "_")


def make_md5(n: str):
    return hashlib.md5(n.encode()).hexdigest()


def make_uuid(username: str = ""):
    return username + str(uuid.uuid4()).replace("-", "")


def check_folder():
    required_folders = ["replays", "beatmaps"]

    if not os.path.isdir("data"):
        os.mkdir("data")

    for folder in required_folders:
        if not os.path.isdir(f"data/{folder}"):
            os.mkdir(f"data/{folder}")


def check_md5(n: str, md5: str):
    return hashlib.md5(n.encode()).hexdigest() == md5


async def send_webhook(
    url, content, isEmbed=False, title=None, title_url=None, thumbnail=None, footer=None
):
    webhook = discord_webhook.AsyncDiscordWebhook(url=url)
    if isEmbed is not False:
        embed = discord_webhook.DiscordEmbed(title=title, description=content)
        embed.set_url(title_url) if title_url != None else ""
        embed.set_thumbnail(thumbnail) if thumbnail != None else ""
        embed.set_footer(footer) if footer != None else ""
        webhook.add_embed(embed)
        try:
            await webhook.execute()
        except Exception:
            return print("Error while sending webhook")
        return print("Embed Webhook sent successfully")
    webhook.set_content(content)
    try:
        await webhook.execute()
        print("Webhook sent successfully ")
    except Exception:
        return print("Error while sending webhook")


async def get_countries():
    countries = await glob.db.fetchall(
        "SELECT DISTINCT country FROM users WHERE country IS NOT NULL ORDER BY country"
    )
    return [row["country"] for row in countries]


def is_convertable(value, type):
    try:
        type(value)
        return True
    except ValueError:
        return False


def timer(func):
    import time

    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        logging.debug(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


def get_country_from_ip(ip_address: str) -> str | None:
    """
    Get country code from IP address using GeoLite2 database or online API.
    Returns ISO country code (e.g., 'US', 'BR') or None if not found/fails.
    """
    # Skip localhost/private IPs
    if (
        ip_address.startswith(("127.", "192.168.", "10.", "172."))
        or ip_address == "::1"
    ):
        return None

    # Try local GeoLite2 database first
    try:
        if os.path.exists("GeoLite2-Country.mmdb"):
            with geoip2.database.Reader("GeoLite2-Country.mmdb") as reader:
                response = reader.country(ip_address)
                country_code = response.country.iso_code
                if country_code and len(country_code) == 2:
                    return country_code
    except Exception as e:
        logging.debug(f"GeoLite2 lookup failed for IP {ip_address}: {e}")

    # Fallback to online API (ipapi.co)
    try:
        import requests

        response = requests.get(f"https://ipapi.co/{ip_address}/country/", timeout=5)
        if response.status_code == 200:
            country_code = response.text.strip()
            if country_code and len(country_code) == 2 and country_code != "Undefined":
                return country_code
    except Exception as e:
        logging.debug(f"Online API lookup failed for IP {ip_address}: {e}")

    return None


async def get_country_from_ip_async(ip_address: str) -> str | None:
    """
    Async version of get_country_from_ip using aiohttp for online API calls.
    """
    # Skip localhost/private IPs
    if (
        ip_address.startswith(("127.", "192.168.", "10.", "172."))
        or ip_address == "::1"
    ):
        return None

    # Try local GeoLite2 database first
    try:
        if os.path.exists("GeoLite2-Country.mmdb"):
            with geoip2.database.Reader("GeoLite2-Country.mmdb") as reader:
                response = reader.country(ip_address)
                country_code = response.country.iso_code
                if country_code and len(country_code) == 2:
                    return country_code
    except Exception as e:
        logging.debug(f"GeoLite2 lookup failed for IP {ip_address}: {e}")

    # Fallback to online API (ipapi.co) using aiohttp
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://ipapi.co/{ip_address}/country/", timeout=5
            ) as response:
                if response.status == 200:
                    country_code = (await response.text()).strip()
                    if (
                        country_code
                        and len(country_code) == 2
                        and country_code != "Undefined"
                    ):
                        return country_code
    except Exception as e:
        logging.debug(f"Online API lookup failed for IP {ip_address}: {e}")

    return None


async def update_user_country_if_needed(user_id: int, ip_address: str):
    """
    Update user's country in database if they don't have one set.
    Uses IP geolocation to determine country.
    """
    try:
        # Check if user already has a country set
        user_data = await glob.db.fetch(
            "SELECT country FROM users WHERE id = $1", [user_id]
        )
        if not user_data or user_data.get("country"):
            return  # User already has country set

        # Try to get country from IP
        country = await get_country_from_ip_async(ip_address)
        if country:
            await glob.db.execute(
                "UPDATE users SET country = $1 WHERE id = $2", [country, user_id]
            )
            logging.info(
                f"Updated country for user {user_id} to {country} based on IP {ip_address}"
            )

    except Exception as e:
        logging.error(f"Failed to update country for user {user_id}: {e}")
