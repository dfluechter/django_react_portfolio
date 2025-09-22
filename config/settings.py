"""
Django settings for the portfolio project.

This module dynamically imports settings from either `settings_dev.py`
or `settings_prod.py` based on the `DJANGO_ENV` environment variable.
"""
import os

# Standard: Entwicklung
env = os.environ.get("DJANGO_ENV", "dev")

if env == "prod":
    from .settings_prod import *
else:
    from .settings_dev import *
