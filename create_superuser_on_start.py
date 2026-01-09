import os
import django

# Sicherstellen, dass Django geladen wird, um auf User-Modelle zugreifen zu können
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') 
django.setup()

from django.contrib.auth.models import User

def create_initial_superuser():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

    if username and password:
        if not User.objects.filter(username=username).exists():
            print("Erstelle initialen Django Superuser...")
            User.objects.create_superuser(username, email, password)
            print(f"Superuser '{username}' erfolgreich erstellt.")
        else:
            print(f"Superuser '{username}' existiert bereits. Übersprungen.")
    else:
        print("Keine Superuser-Variablen gefunden. Übersprungen.")

if __name__ == '__main__':
    create_initial_superuser()