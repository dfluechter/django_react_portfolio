import factory
import factory.fuzzy
from portfolio.models import CertificateIssuer, Project, Technology, Certificate
from django.contrib.auth.models import User

# --- Utility Functions and Binary Data ---
PDF_CONTENT = b"%PDF-1.4\n%Minimal content for testing purposes.\n%%EOF"

# --- Factories ---


class CertificateIssuerFactory(factory.django.DjangoModelFactory):
    class Meta:
        # Hier stand vorher models.CertificateIssuer -> Das war der Fehler!
        model = CertificateIssuer

    name = factory.Sequence(lambda n: f"Issuer {n}")


class TechnologyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Technology

    name = factory.Sequence(lambda n: f"Tech Name {n}")
    slug = None


class CertificateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Certificate

    name = factory.Faker("catch_phrase")
    category = factory.Faker("word")
    issue_date = factory.Faker("past_date")
    issuer = factory.SubFactory(CertificateIssuerFactory)
    # Nutzt den PDF_CONTENT von oben, um Validierungen zu bestehen
    pdf_file = factory.django.FileField(
        filename="valid_certificate.pdf", data=PDF_CONTENT
    )


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence(lambda n: f"Project Alpha {n}")
    slug = None
    title = factory.Faker("catch_phrase")
    description = factory.Faker("text")

    # Korrektur für Status: Wir nutzen den Import direkt
    status = factory.fuzzy.FuzzyChoice(Project.Status.values)

    image = factory.django.ImageField(
        filename="project_image.jpg", width=100, height=100
    )

    @factory.post_generation
    def technologies(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tech in extracted:
                self.technologies.add(tech)
        else:
            techs = TechnologyFactory.create_batch(2)
            self.technologies.add(*techs)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
