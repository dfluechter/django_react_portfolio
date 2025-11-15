# 🌐 Django + Tailwind Portfolio

![Python](https://img.shields.io/badge/Python-3.13-orange?style=plastic&logo=python)
![Django](https://img.shields.io/badge/Django-5.2.8-092E20?style=plastic&logo=django)
[![Django CI](https://github.com/dfluechter/django_react_portfolio/actions/workflows/django-ci.yml/badge.svg)](https://github.com/dfluechter/django_react_portfolio/actions/workflows/django-ci.yml)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?style=plastic&logo=tailwind-css)
![Status](https://img.shields.io/badge/status-in_progress-yellow?style=plastic&color=red)

> ✨ Ein modernes, responsives Portfolio mit Django, Tailwind, Dark Mode, Burger-Menü und Auth via Djoser.

---

## 🚀 Features

- 🔐 Authentifizierung mit **Djoser**
- 🌙 **Dark Mode** Toggle (persistent)
- 🍔 **Burger-Menü** mit animierter Sidebar
- 🧾 Admin-Bereich + Lebenslauf + Zertifikate + Projekte
- 💅 Stylisch mit **Tailwind CSS**
- ⚙️ Fullscreen Mobile-Nav
- ✅ MIT-lizenziert

---

## 🔧 Tech Stack

| Kategorie  | Technologie                              |
| ---------- | ---------------------------------------- |
| Backend    | Django 5.2.8                             |
| Frontend   | Tailwind CSS 3                           |
| Auth       | Djoser (Token)                           |
| Styling    | Alpine.js, FontAwesome                   |
| Deployment | Render (Web Service), Netlify (Database) |

---

## 🛠️ Setup

```bash
git clone https://github.com/dfluechter/django_react_portfolio.git
cd django_react_portfolio
python -m venv .venv
source .venv/bin/activate  # oder .\.venv\Scripts\activate auf Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🚀 Deployment

This project is configured for deployment on Render, with the database hosted on Netlify.

### 1. Database Setup (Netlify)

1. **Create a new PostgreSQL database** on your chosen platform (e.g., Netlify, Supabase, ElephantSQL).
2. **Locate the connection string (URL)** for your database. It should look something like this: `postgresql://user:password@host:port/dbname`.

### 2. Web Service Setup (Render)

1. **Fork this repository** and create a new "Web Service" on Render, connecting it to your fork.
2. In the Render dashboard, go to the "Environment" settings for your web service.
3. **Add a new environment variable** with the key `DATABASE_URL`.
4. For the value, **paste the connection string** from your Netlify database.
5. Ensure the `DJANGO_ENV` environment variable is set to `prod` for production.
6. Render will use the `render.yaml` file to automatically configure the build and start commands. Your application should deploy and connect to your external database.
