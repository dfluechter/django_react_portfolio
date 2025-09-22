"""
Tests for the portfolio models.
"""
import pytest
from portfolio.models import Project, Certificate
from .factories import UserFactory, ProjectFactory, CertificateFactory

pytestmark = pytest.mark.django_db  # Enable DB for all tests

def test_create_user():
    """
    Tests the creation of a user.
    """
    user = UserFactory()
    assert user.pk is not None
    assert user.username is not None

def test_create_project():
    """
    Tests the creation of a project.
    """
    project = ProjectFactory()
    assert project.pk is not None
    assert project.name != ''

def test_create_certificate():
    """
    Tests the creation of a certificate.
    """
    certificate = CertificateFactory()
    assert certificate.pk is not None
    assert certificate.name != ''
