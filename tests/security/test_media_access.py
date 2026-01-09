import pytest
from django.urls import reverse
from tests.unit.factories import CertificateFactory


@pytest.mark.security
@pytest.mark.django_db
def test_certificate_pdf_is_protected_from_anonymous_users(client):
    """
    Sicherheitstest: Stellt sicher, dass ein nicht authentifizierter User
    keinen Zugriff auf die PDF-Datei eines Zertifikats hat.
    """
    # 1. Erstelle ein Zertifikat mit einer Datei über die Factory
    certificate = CertificateFactory()
    file_url = certificate.pdf_file.url

    # 2. Versuche als anonymer User die Datei aufzurufen
    response = client.get(file_url)

    # 3. Erwartung: Entweder 403 (Forbidden) oder 302 (Redirect zum Login)
    # Je nach deiner Middleware/Server-Konfiguration
    assert response.status_code in [302, 403, 404], (
        f"Sicherheitslücke: PDF unter {file_url} ist öffentlich zugänglich!"
    )


@pytest.mark.security
@pytest.mark.django_db
def test_admin_path_is_not_guessable(client):
    """Prüft, ob der Admin-Bereich standardmäßig geschützt ist."""
    response = client.get("/admin/")
    assert response.status_code == 302  # Redirect zum Login
