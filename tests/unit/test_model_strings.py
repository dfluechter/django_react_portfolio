import pytest
from portfolio.admin import CertificateAdmin, ProjectAdmin
from tests.unit.factories import (
    TechnologyFactory, ProjectFactory, CertificateFactory, CertificateIssuerFactory
)

@pytest.mark.django_db
def test_model_str_representations():
    """Testet die __str__ Methoden aller Models für 100% Coverage."""
    tech = TechnologyFactory(name="Python")
    assert str(tech) == "Python"
    
    issuer = CertificateIssuerFactory(name="Udemy")
    assert str(issuer) == "Udemy"
    
    project = ProjectFactory(name="My Portfolio")
    assert str(project) == "My Portfolio"
    
    cert = CertificateFactory(name="Django Cert", issuer=issuer)
    # Falls dein Cert-String 'Name - Issuer' ist:
    assert str(cert) == f"Django Cert"