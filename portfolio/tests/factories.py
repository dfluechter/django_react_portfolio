import factory
from django.contrib.auth.models import User
from portfolio.models import Project, Certificate  # Beispielmodelle

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')


class CertificateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Certificate

    name = factory.Faker('sentence', nb_words=2)
    issuer = factory.Faker('company')
