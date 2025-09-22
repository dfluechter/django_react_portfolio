# portfolio/management/commands/import_certificates.py
import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from portfolio.models import Certificate, CertificateIssuer
from django.core.files import File

CERT_DIR = "media/certificates"

class Command(BaseCommand):
    help = "Importiere alle PDFs aus /media/certificates/<issuer>/..."

    def handle(self, *args, **kwargs):
        base_path = os.path.abspath(CERT_DIR)

        for issuer_folder in os.listdir(base_path):
            issuer_path = os.path.join(base_path, issuer_folder)

            if not os.path.isdir(issuer_path):
                continue

            issuer_name = issuer_folder.replace("-", " ").title()
            issuer, created = CertificateIssuer.objects.get_or_create(name=issuer_name)

            for filename in os.listdir(issuer_path):
                if not filename.lower().endswith(".pdf"):
                    continue

                file_path = os.path.join(issuer_path, filename)

                cert_name = os.path.splitext(filename)[0].replace("_", " ").title()

                # Falls das Zertifikat schon da ist, skippen
                if Certificate.objects.filter(name=cert_name, issuer=issuer).exists():
                    continue

                # Erstellen
                with open(file_path, "rb") as f:
                    django_file = File(f)
                    cert = Certificate(
                        name=cert_name,
                        category="Auto-Import",
                        issue_date="2024-01-01",  # Platzhalter
                        expiry_date=None,
                        issuer=issuer
                    )
                    cert.pdf_file.save(filename, django_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f"Importiert: {cert_name}"))
