# 🌐 Django + Tailwind Portfolio

![Python](https://img.shields.io/badge/Python-3.13-orange?style=plastic&logo=python)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=plastic&logo=django)
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

| Kategorie  | Technologie            |
| ---------- | ---------------------- |
| Backend    | Django 5.2             |
| Frontend   | Tailwind CSS 3         |
| Auth       | Djoser (Token)         |
| Styling    | Alpine.js, FontAwesome |
| Deployment | coming soon...         |

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
