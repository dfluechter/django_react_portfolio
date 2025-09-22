import pytest
from django.core.management import call_command
from io import StringIO
from portfolio.models import Certificate, CertificateIssuer
import tempfile
import os
from pathlib import Path

@pytest.mark.django_db
def test_import_certificates_command(monkeypatch):
    with tempfile.TemporaryDirectory() as tempdir:
        # Mock the CERT_DIR constant
        monkeypatch.setattr('portfolio.management.commands.import_certificates.CERT_DIR', tempdir)

        # Create a dummy issuer folder and pdf file
        issuer_folder = Path(tempdir) / "test-issuer"
        issuer_folder.mkdir()
        pdf_file = issuer_folder / "test_certificate.pdf"
        pdf_file.touch()

        # Run the command
        out = StringIO()
        call_command('import_certificates', stdout=out)

        # Check that the issuer and certificate were created
        assert CertificateIssuer.objects.count() == 1
        assert Certificate.objects.count() == 1
        issuer = CertificateIssuer.objects.first()
        assert issuer.name == "Test Issuer"
        certificate = Certificate.objects.first()
        assert certificate.name == "Test Certificate"
        assert certificate.issuer == issuer
        assert out.getvalue().strip() == "Importiert: Test Certificate"

        # Run the command again to check for duplicates
        out = StringIO()
        call_command('import_certificates', stdout=out)
        assert Certificate.objects.count() == 1
        assert out.getvalue() == ""
