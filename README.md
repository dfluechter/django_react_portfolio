# 🌐 Django + Tailwind Portfolio

![MIT License](https://img.shields.io/github/license/dfluechter/django_react_portfolio?style=flat-square)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?style=flat-square&logo=tailwind-css)
![Status](https://img.shields.io/badge/status-in_progress-yellow?style=flat-square)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)

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

| Kategorie     | Technologie       |
|--------------|-------------------|
| Backend      | Django 5.2        |
| Frontend     | Tailwind CSS 3    |
| Auth         | Djoser (Token)    |
| Styling      | Alpine.js, FontAwesome |
| Deployment   | coming soon...    |

---

## 🛠️ Setup

```bash
git clone https://github.com/dfluechter/django_react_portfolio.git
cd django_react_portfolio
python -m venv env
source env/bin/activate  # oder .\env\Scripts\activate auf Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
