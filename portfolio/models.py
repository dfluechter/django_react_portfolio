# portfolio/models.py
from django.db import models
from django.utils.text import slugify

def certificate_upload_path(instance, filename):
    # slugify sorgt für saubere Ordnernamen
    issuer_slug = slugify(instance.issuer.name)
    return f"certificates/{issuer_slug}/{filename}"

class Certificate(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    issuer = models.ForeignKey("CertificateIssuer", on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to=certificate_upload_path)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name
    
class CertificateIssuer(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

def project_image_upload_path(instance, filename):
    # slugify sorgt für saubere Ordnernamen
    project_slug = slugify(instance.name)
    return f"projects/{project_slug}/images/{filename}"

class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    STATUS_CHOICES = (
        ("in_progress", "In Arbeit"),
        ("completed", "Abgeschlossen"),
        ("archived", "Archiviert"),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to=project_image_upload_path, blank=True, null=True)
    live_url = models.URLField(blank=True)
    repository_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_progress")
    created_at = models.DateTimeField(auto_now_add=True)
    technologies = models.ManyToManyField(Technology, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
