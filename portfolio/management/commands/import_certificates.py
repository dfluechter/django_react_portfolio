# portfolio/management/commands/import_certificates.py
"""
Django management command to import certificates from a directory.
"""
import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from portfolio.models import Certificate, CertificateIssuer
from django.core.files import File

CERT_DIR = "media/certificates"

class Command(BaseCommand):
    """
    Django management command to import certificates from a directory.
    """
    help = "Imports all PDFs from /media/certificates/<issuer>/..."

    def handle(self, *args, **kwargs):
        """
        Handles the import of certificates.
        """
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

                # Skip if the certificate already exists
                if Certificate.objects.filter(name=cert_name, issuer=issuer).exists():
                    continue

                # Create the certificate
                with open(file_path, "rb") as f:
                    django_file = File(f)
                    cert = Certificate(
                        name=cert_name,
                        category="Auto-Import",
                        issue_date="2024-01-01",  # Placeholder
                        expiry_date=None,
                        issuer=issuer
                    )
                    cert.pdf_file.save(filename, django_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f"Imported: {cert_name}"))
