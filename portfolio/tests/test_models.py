import pytest
from django.utils.text import slugify
from portfolio.models import Project, Certificate, Technology
from .factories import UserFactory, ProjectFactory, CertificateFactory, TechnologyFactory

pytestmark = pytest.mark.django_db

def test_create_user():
    user = UserFactory()
    assert user.pk is not None
    assert user.username is not None

def test_create_technology():
    tech = TechnologyFactory(name="Test Tech")
    assert tech.pk is not None
    assert tech.name == "Test Tech"
    assert tech.slug == "test-tech"

def test_create_project():
    project = ProjectFactory(name="My Awesome Project")
    assert project.pk is not None
    assert project.name == "My Awesome Project"
    assert project.slug == "my-awesome-project"
    assert project.status in [choice[0] for choice in Project.STATUS_CHOICES]
    assert project.technologies.count() > 0

def test_project_slug_creation():
    project = Project(name="A Project Without a Slug")
    project.save()
    assert project.slug == slugify(project.name)

def test_create_certificate():
    certificate = CertificateFactory()
    assert certificate.pk is not None
    assert certificate.name != ''
    assert certificate.issuer is not None
