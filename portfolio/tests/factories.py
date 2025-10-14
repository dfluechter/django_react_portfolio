import factory
from django.contrib.auth import get_user_model
from portfolio.models import Certificate, CertificateIssuer, Project, Technology

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

class TechnologyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Technology

    name = factory.Sequence(lambda n: f"Technology {n}")

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f"Project {n}")
    description = factory.Faker('paragraph')
    status = factory.Iterator([choice[0] for choice in Project.STATUS_CHOICES])
    live_url = factory.Faker('url')
    repository_url = factory.Faker('url')

    @factory.post_generation
    def technologies(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tech in extracted:
                self.technologies.add(tech)
        else:
            # Add 2 random technologies if none are provided
            techs = TechnologyFactory.create_batch(2)
            self.technologies.add(*techs)

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