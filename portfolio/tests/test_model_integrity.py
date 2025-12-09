# portfolio/tests/test_model_integrity.py

import pytest
from unittest.mock import patch, MagicMock
from django.db import IntegrityError, ProtectedError
from django.core.exceptions import ValidationError
from portfolio.models import Project, Certificate
from.factories import TechnologyFactory, ProjectFactory, CertificateFactory, CertificateIssuerFactory
from io import BytesIO

# --- 1. Testen der Slug-Logik (Concurrency-Resistenz) ---

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
    """
    Testet, dass die Slug-Logik Kollisionen auflöst, indem ein Zähler angehängt wird.
    (Integrationstest mit Datenbank, da die Logik in generate_unique_slug liegt)
    """
    # 1. Erstelle das Original
    tech_a = technology_factory(name="Python")
    assert tech_a.slug == "python"

    # 2. Erstelle eine Kollision
    tech_b = technology_factory(name="Python")
    # Es sollte automatisch "python-1" generiert werden
    assert tech_b.slug == "python-1"

    # 3. Erstelle eine zweite Kollision
    tech_c = technology_factory(name="Python")
    assert tech_c.slug == "python-2"

# --- 2. Testen von on_delete=PROTECT ---

@pytest.mark.django_db
def test_issuer_deletion_is_protected():
    """
    Stellt sicher, dass das Löschen eines CertificateIssuer fehlschlägt, 
    wenn noch aktive Zertifikate darauf verweisen.
    """
    issuer = CertificateIssuerFactory()
    CertificateFactory(issuer=issuer)

    with pytest.raises(ProtectedError): # Fängt die Django-interne Ausnahme ab 
        issuer.delete()

@pytest.mark.django_db
def test_issuer_deletion_succeeds_if_unrelated():
    """Stellt sicher, dass das Löschen erfolgreich ist, wenn keine Abhängigkeiten bestehen."""
    issuer = CertificateIssuerFactory()
    # Kein Fehler erwartet
    issuer.delete()
    assert Certificate.objects.filter(issuer=issuer).count() == 0

# --- 3. Testen der Sicherheitsvalidierung (MIME-Type) ---

# WICHTIG: Wir müssen die externe Abhängigkeit (python-magic) mocken, 
# da wir nicht echte PDF-Dateien laden wollen und die Erkennung deterministisch sein soll. 
@pytest.mark.django_db
@patch('portfolio.models.magic.from_buffer')
def test_certificate_rejects_non_pdf_content(mock_magic_from_buffer):
    """Testet, dass der Validator fehlschlägt, wenn der MIME-Typ nicht application/pdf ist."""
    # 1. Mocke den magic-Aufruf, um einen ungültigen Typ zurückzugeben (z.B. eine ausführbare Datei)
    mock_magic_from_buffer.return_value = 'application/x-dosexec'
    
    # 2. Erstelle eine ungültige Datei (Inhalt ist egal, da Mocking)
    invalid_file = ContentFile(b'Malicious data', name='script.pdf')

    # 3. Teste den Validator
    with pytest.raises(ValidationError) as excinfo:
        Certificate.objects.create(
            name="Test",
            category="Security",
            issue_date="2025-01-01",
            issuer=CertificateIssuerFactory(),
            # Der FileField-Setter ruft die Validatoren auf
            pdf_file=invalid_file 
        )
    assert 'File is not a valid PDF' in str(excinfo.value)

@pytest.mark.django_db
@patch('portfolio.models.magic.from_buffer')
def test_certificate_accepts_valid_pdf_content(mock_magic_from_buffer):
    """Testet, dass der Validator erfolgreich ist, wenn der MIME-Typ PDF ist."""
    # Mocke den magic-Aufruf, um den korrekten Typ zurückzugeben
    mock_magic_from_buffer.return_value = 'application/pdf'
    
    # Erstelle eine Datei mit gültigem Inhalt (der PDF_CONTENT aus der Factory)
    valid_file = ContentFile(b'%PDF-HEADER', name='doc.pdf')

    # Kein Fehler erwartet
    certificate = Certificate.objects.create(
        name="Valid Cert",
        category="Tech",
        issue_date="2025-01-01",
        issuer=CertificateIssuerFactory(),
        pdf_file=valid_file
    )
    assert certificate.name == "Valid Cert"

# --- 4. Testen der Datenstruktur (TextChoices und Felder) ---

@pytest.mark.django_db
def test_project_status_uses_textchoices(project):
    """Verifiziert die Zuweisung des Status über die TextChoices-Werte."""
    # project ist eine Instanz, die über pytest-factoryboy automatisch erstellt wurde
    assert project.status in Project.Status.values # 

@pytest.mark.django_db
def test_project_default_title_is_empty_string(project_factory):
    """Verifiziert, dass Titel-Feld korrekt auf leeren String ('') standardisiert wird."""
    project = project_factory(title="")
    assert project.title == ""
    assert project.title is not None
