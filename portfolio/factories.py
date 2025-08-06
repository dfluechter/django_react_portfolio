# portfolio/factories.py
import factory
from portfolio.models import Certificate, CertificateIssuer, Project
from django.core.files.base import ContentFile

class CertificateIssuerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CertificateIssuer

    name = factory.Faker("company")


class CertificateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Certificate

    name = factory.Faker("job")
    category = factory.Faker("word")
    issue_date = factory.Faker("date_this_decade")
    expiry_date = None
    issuer = factory.SubFactory(CertificateIssuerFactory)
    pdf_file = factory.django.FileField(filename="example.pdf", data=b"PDF content")
    url = "https://example.com"


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker("sentence", nb_words=3)
    url = "https://example.com"
    created_at = factory.Faker("date_this_year")
    description = factory.Faker("text")
