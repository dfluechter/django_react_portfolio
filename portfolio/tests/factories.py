"""
Factories for the portfolio app.
"""
import factory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from portfolio.models import Certificate, CertificateIssuer, Project

class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for the User model.
    """
    class Meta:
        model = get_user_model()
        skip_postgeneration_save = True

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class ProjectFactory(factory.django.DjangoModelFactory):
    """
    Factory for the Project model.
    """
    class Meta:
        model = Project

    name = factory.Faker('sentence', nb_words=3)
    url = factory.Faker('url')
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')

class CertificateIssuerFactory(factory.django.DjangoModelFactory):
    """
    Factory for the CertificateIssuer model.
    """
    class Meta:
        model = CertificateIssuer
    name = factory.Faker('company')
    
class CertificateFactory(factory.django.DjangoModelFactory):
    """
    Factory for the Certificate model.
    """
    class Meta:
        model = Certificate
    issue_date = factory.Faker('past_date')
    issuer = factory.SubFactory(CertificateIssuerFactory)
    name = factory.Faker('catch_phrase')