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

class Project(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name
