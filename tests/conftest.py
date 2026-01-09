import pytest
from pytest_factoryboy import register
from tests.unit.factories import (
    UserFactory,
    ProjectFactory,
    TechnologyFactory,
    CertificateFactory,
    CertificateIssuerFactory,
)

# Registriert die Factories als Fixtures für alle Tests
register(UserFactory)
register(ProjectFactory)
register(TechnologyFactory)
register(CertificateFactory)
register(CertificateIssuerFactory)


@pytest.fixture
def api_client():
    from django.test import Client

    return Client()
