import factory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from portfolio.models import Certificate, CertificateIssuer, Project # Beispielmodelle

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        skip_postgeneration_save = True

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')

class CertificateIssuerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CertificateIssuer
    name = factory.Faker('company')
    
class CertificateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Certificate
    issue_date = factory.Faker('past_date')
    issuer = factory.SubFactory(CertificateIssuerFactory)
    name = factory.Faker('catch_phrase')