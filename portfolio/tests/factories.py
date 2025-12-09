# portfolio/tests/factories.py

import factory
import factory.fuzzy
from django.core.files.base import ContentFile
from portfolio import models

# --- Utility Functions and Binary Data ---

# Minimaler PDF-Header (Magic Bytes: %PDF-) für die Validierung
# Dies ist notwendig, da der Model Validator prüft, ob die Datei ein echtes PDF ist.
PDF_CONTENT = b'%PDF-1.4\n%Minimal content for testing purposes.\n%%EOF'

# --- Factories ---

class CertificateIssuerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CertificateIssuer
        # Fügen Sie ein Factory-Feld für den Namen hinzu, um Unique-Constraints zu gewährleisten
        name = factory.Sequence(lambda n: f"Issuer {n}")

class CertificateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Certificate

    name = factory.Faker('word')
    category = factory.Faker('job')
    issue_date = factory.Faker('date_this_year')
    issuer = factory.SubFactory(CertificateIssuerFactory)
    url = factory.Faker('url')

    # Erzeugt eine gültige Datei mit PDF Magic Bytes
    pdf_file = factory.django.FileField(
        filename='valid_certificate.pdf',
        data=PDF_CONTENT
    )

class TechnologyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Technology

    name = factory.Sequence(lambda n: f"Tech Name {n}")
    # Der Slug wird von der Model-save()-Methode automatisch generiert, 
    # wir können ihn hier weglassen oder None setzen, um die Logik zu testen.
    slug = None 

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Project

    name = factory.Sequence(lambda n: f"Project Alpha {n}")
    slug = None
    title = factory.Faker('catch_phrase')
    description = factory.Faker('text')

    # Auswahl eines zufälligen Werts aus der TextChoices-Enumeration
    status = factory.fuzzy.FuzzyChoice(models.Project.Status.values)

    # ImageField nutzt ImageField, was automatisch gültige Bildbytes erzeugt,
    # die unsere ImageField-Validierung bestehen.
    image = factory.django.ImageField(filename='project_image.jpg', width=100, height=100)

    # Viele-zu-Viele-Beziehungen (M2M) müssen nach der Erstellung verwaltet werden (post_generation)
    @factory.post_generation
    def technologies(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # Falls Technologielisten beim Factory-Aufruf explizit übergeben wurden
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
    
    name = factory.Faker('catch_phrase')
    category = factory.Faker('word')
    issue_date = factory.Faker('past_date')
    issuer = factory.SubFactory(CertificateIssuerFactory)
    pdf_file = factory.django.FileField(filename='certificate.pdf')