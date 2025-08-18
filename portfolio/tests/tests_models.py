import pytest
from portfolio.models import Project, Certificate
from .factories import UserFactory, ProjectFactory, CertificateFactory

pytestmark = pytest.mark.django_db  # DB für alle Tests aktivieren

def test_create_user():
    user = UserFactory()
    assert user.pk is not None
    assert user.username is not None

def test_create_project():
    project = ProjectFactory()
    assert project.pk is not None
    assert project.title != ''

def test_create_certificate():
    certificate = CertificateFactory()
    assert certificate.pk is not None
    assert certificate.name != ''
