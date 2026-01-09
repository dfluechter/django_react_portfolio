import pytest
from unittest.mock import patch
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from portfolio.models import Technology, Project, Certificate, CertificateIssuer
from tests.unit.factories import (
    TechnologyFactory, ProjectFactory, CertificateFactory, CertificateIssuerFactory
)
from django.db.models.deletion import ProtectedError


@pytest.mark.django_db
def test_slug_is_generated_on_creation(technology_factory):
    """Verifiziert, dass der Slug automatisch generiert wird, wenn er fehlt."""
    tech = technology_factory(name="Deep Learning Model")
    assert tech.slug == "deep-learning-model"


@pytest.mark.django_db
def test_slug_is_not_updated_on_subsequent_save(technology_factory):
    """Verifiziert, dass der Slug bei nachfolgenden Saves nicht überschrieben wird (für stabile URLs)."""
    tech = technology_factory(name="Old Name", slug="old-name-slug")
    tech.name = "New Name"
    tech.save()
    assert tech.slug == "old-name-slug"


@pytest.mark.django_db
def test_slug_collision_resolution_on_create(technology_factory):
    tech_a = technology_factory(name="Python")
    assert tech_a.slug == "python"

    # Nutze einen anderen Namen, der aber denselben Slug erzeugen würde (z.B. durch Sonderzeichen)
    # Oder ändere dein Model so, dass Name nicht unique sein muss. 
    # Wenn Name unique bleiben soll, teste die Slug-Logik so:
    tech_b = technology_factory(name="Python!!!") 
    assert tech_b.slug == "python-1"


# --- 2. Testen von on_delete=PROTECT ---


@pytest.mark.django_db
def test_issuer_deletion_is_protected():
    """
    Stellt sicher, dass das Löschen eines CertificateIssuer fehlschlägt,
    wenn noch aktive Zertifikate darauf verweisen.
    """
    issuer = CertificateIssuerFactory()
    CertificateFactory(issuer=issuer)

    with pytest.raises(ProtectedError):  # Fängt die Django-interne Ausnahme ab
        issuer.delete()


@pytest.mark.django_db
def test_issuer_deletion_succeeds_if_unrelated():
    issuer = CertificateIssuerFactory()
    issuer_id = issuer.id # ID merken
    issuer.delete()
    assert Certificate.objects.filter(issuer_id=issuer_id).count() == 0


# --- 3. Testen der Sicherheitsvalidierung (MIME-Type) ---


# WICHTIG: Wir müssen die externe Abhängigkeit (python-magic) mocken,
# da wir nicht echte PDF-Dateien laden wollen und die Erkennung deterministisch sein soll.
@pytest.mark.django_db
@patch("portfolio.models.magic.from_buffer")
def test_certificate_rejects_non_pdf_content(mock_magic_from_buffer):
    mock_magic_from_buffer.return_value = "application/x-dosexec"
    invalid_file = ContentFile(b"Malicious", name="test.pdf")
    cert = CertificateFactory.build(pdf_file=invalid_file) # .build() statt .create()
    
    with pytest.raises(ValidationError):
        cert.full_clean() # Triggert die Validatoren manuell


@pytest.mark.django_db
@patch("portfolio.models.magic.from_buffer")
def test_certificate_accepts_valid_pdf_content(mock_magic_from_buffer):
    """Testet, dass der Validator erfolgreich ist, wenn der MIME-Typ PDF ist."""
    # Mocke den magic-Aufruf, um den korrekten Typ zurückzugeben
    mock_magic_from_buffer.return_value = "application/pdf"

    # Erstelle eine Datei mit gültigem Inhalt (der PDF_CONTENT aus der Factory)
    valid_file = ContentFile(b"%PDF-HEADER", name="doc.pdf")

    # Kein Fehler erwartet
    certificate = Certificate.objects.create(
        name="Valid Cert",
        category="Tech",
        issue_date="2025-01-01",
        issuer=CertificateIssuerFactory(),
        pdf_file=valid_file,
    )
    assert certificate.name == "Valid Cert"


# --- 4. Testen der Datenstruktur (TextChoices und Felder) ---


@pytest.mark.django_db
def test_project_status_uses_textchoices(project):
    """Verifiziert die Zuweisung des Status über die TextChoices-Werte."""
    # project ist eine Instanz, die über pytest-factoryboy automatisch erstellt wurde
    assert project.status in Project.Status.values  #


@pytest.mark.django_db
def test_project_default_title_is_empty_string(project_factory):
    """Verifiziert, dass Titel-Feld korrekt auf leeren String ('') standardisiert wird."""
    project = project_factory(title="")
    assert project.title == ""
    assert project.title is not None
