# 🌐 Django + Tailwind Portfolio

![Python](https://img.shields.io/badge/Python-3.13-orange?style=plastic&logo=python)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=plastic&logo=django)
[![Django CI](https://github.com/dfluechter/django_react_portfolio/actions/workflows/django-ci.yml/badge.svg)](https://github.com/dfluechter/django_react_portfolio/actions/workflows/django-ci.yml)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?style=plastic&logo=tailwind-css)
![Status](https://img.shields.io/badge/status-in_progress-yellow?style=plastic&color=red)

> ✨ A modern, responsive portfolio built with Django, Tailwind CSS, Dark Mode, a Burger Menu, and authentication via Djoser.

This project is a personal portfolio website designed to showcase projects, certificates, and a CV. It is built with a modern tech stack and features a clean, responsive design.

---

## 🚀 Features

- 🔐 **Authentication**: Secure authentication powered by **Djoser**.
- 🌙 **Dark Mode**: Toggle between light and dark modes (persistent).
- 🍔 **Burger Menu**: Animated sidebar for easy navigation on mobile devices.
- 🧾 **Admin Area**: Manage your portfolio content with ease.
- 💅 **Styling**: Beautifully styled with **Tailwind CSS**.
- ⚙️ **Fullscreen Mobile Navigation**: A seamless experience on any device.
- ✅ **MIT Licensed**: Open source and free to use.

---

## 🔧 Tech Stack

| Category   | Technology             |
| ---------- | ---------------------- |
| Backend    | Django 5.2             |
| Frontend   | Tailwind CSS 3         |
| Auth       | Djoser (Token)         |
| Styling    | Alpine.js, FontAwesome |
| Deployment | coming soon...         |

---

## 🛠️ Setup

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.13 or later
- pip

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/dfluechter/django_react_portfolio.git
    ```
2.  Navigate to the project directory
    ```sh
    cd django_react_portfolio
    ```
3.  Create a virtual environment
    ```sh
    python -m venv .venv
    ```
4.  Activate the virtual environment

    -   On Windows, run:
        ```sh
        .venv\Scripts\activate
        ```
    -   On macOS and Linux, run:
        ```sh
        source .venv/bin/activate
        ```
5.  Install Python packages
    ```sh
    pip install -r requirements.txt
    ```
6.  Apply database migrations
    ```sh
    python manage.py migrate
    ```
7.  Run the development server
    ```sh
    python manage.py runserver
    ```

---

## 🧪 Running Tests

To run the automated tests for this system, use the following command:

```bash
pytest
```

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
