<div align="center">

# OsuZenith Frontend

**A clean, dark, and lightweight frontend for an osu!droid relax server.**

<p>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  </a>
  <a href="https://flask.palletsprojects.com/">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  </a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/HTML">
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  </a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/CSS">
    <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  </a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript">
    <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript" />
  </a>
  <a href="https://git-scm.com/">
    <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" />
  </a>
  <a href="https://github.com/features/actions">
    <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions" />
  </a>
</p>

</div>

---

## About

**OsuZenith Frontend** is the web interface for an **osu!droid relax server**.  
It is built with **Python / Flask**, **HTML templates**, **CSS**, and a small amount of **JavaScript** to keep the server easy to browse, simple to deploy, and pleasant to use.

The site includes the public-facing pages players usually need, such as:

- Home / landing page
- Player profile page
- Leaderboard page
- Login and register pages
- Account settings pages
- Download and community links

The visual style is focused on a dark, rounded, Cupertino-inspired interface with subtle motion, soft depth, and a readable layout.

---

## APK Download

The osu!droid relax client APK is available here:

**[Download the APK from odrx-client releases](https://github.com/hikayune/odrx-client/releases)**

---

## Environment Variables

Create a `.env` file locally or add these variables in your hosting provider, such as Vercel.

```env
# Backend API URL
BACKEND_URL=https://your-backend-url-here.com

# Community / external links
DISCORD_URL=https://discord.gg/your-server
GITHUB_URL=https://github.com/your/repository

# Client download page
CLIENT_DOWNLOAD_URL=https://github.com/hikayune/odrx-client/releases

# Client version shown on the website
CLIENT_VERSION=latest
```

### Variable guide

| Variable | Description |
| --- | --- |
| `BACKEND_URL` | URL of your osu!droid relax backend API. |
| `DISCORD_URL` | Discord invite shown on the frontend. |
| `GITHUB_URL` | Repository or project link shown on the frontend. |
| `CLIENT_DOWNLOAD_URL` | Link used by the download button. |
| `CLIENT_VERSION` | Client version displayed in the welcome section. |

---

## Backend URL

Set your backend URL here:

```env
BACKEND_URL=https://your-backend-url-here.com
```

The frontend uses this value to communicate with your osu!droid relax server backend.  
Make sure the backend is online and accessible from the deployed frontend.

---

## Local Development

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the app locally:

```bash
python app.py
```

Then open the local URL shown in your terminal.

---

## Deployment Notes

When deploying to Vercel or another hosting provider:

1. Add all required environment variables.
2. Make sure `BACKEND_URL` points to your real backend.
3. Redeploy the project after changing environment variables.
4. Replace the header image if you want a custom server icon.

The header image can be replaced here:

```txt
public/static/brand-photo.png
```

Keep the image square for the best result. The frontend will automatically crop it into the correct rounded shape.

---

## Project Structure

```txt
.
├── app.py
├── requirements.txt
├── public/
│   └── static/
│       └── brand-photo.png
└── templates/
    ├── base.html
    ├── main_page.jinja
    ├── leaderboard.jinja
    ├── profile.jinja
    └── account/
```

---


## Maintainer

This frontend is maintained by **[hikayune](https://github.com/hikayune)**.

<p align="center">
  <a href="https://spotify-github-profile.kittinanx.com/api/view?uid=31y3gkslyy4xsszg43x3e5aju3wi&redirect=true">
    <img src="https://spotify-github-profile.kittinanx.com/api/view?uid=31y3gkslyy4xsszg43x3e5aju3wi&cover_image=true&theme=natemoo-re&show_offline=true&background_color=121212&interchange=false&profanity=true&bar_color=53b14f&bar_color_cover=false" alt="Spotify GitHub profile" />
  </a>
</p>

<p align="center">
  <a href="https://github.com/hikayune">
    <img src="https://img.shields.io/badge/GitHub-hikayune-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub profile" />
  </a>
  <a href="https://discord.com/users/1046820194762379274">
    <img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord profile" />
  </a>
  <a href="https://www.last.fm/pt/user/hd_ph7">
    <img src="https://img.shields.io/badge/Last.fm-D51007?style=for-the-badge&logo=lastdotfm&logoColor=white" alt="Last.fm profile" />
  </a>
  <a href="https://osu.ppy.sh/users/34289421">
    <img src="https://img.shields.io/badge/osu!-FF66AA?style=for-the-badge&logo=osu&logoColor=white" alt="osu! profile" />
  </a>
</p>

---

## License

This project uses the license included in this repository.

Please see the repository license file here:

**[Open the repository license](LICENSE)**

---

<div align="center">

Made for **OsuZenith** — an osu!droid relax server frontend.

</div>
