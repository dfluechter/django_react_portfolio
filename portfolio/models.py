# portfolio/models.py
"""
Models for the portfolio app.
"""
from django.db import models
from django.utils.text import slugify

def certificate_upload_path(instance, filename):
    """
    Generates the upload path for certificate files.

    Args:
        instance: The Certificate instance.
        filename (str): The original filename.

    Returns:
        str: The upload path for the certificate file.
    """
    # slugify ensures clean folder names
    issuer_slug = slugify(instance.issuer.name)
    return f"certificates/{issuer_slug}/{filename}"

class Certificate(models.Model):
    """
    Represents a certificate.
    """
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    issuer = models.ForeignKey("CertificateIssuer", on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to=certificate_upload_path)
    url = models.URLField(blank=True)

    def __str__(self):
        """
        Returns the string representation of the certificate.
        """
        return self.name
    
class CertificateIssuer(models.Model):
    """
    Represents a certificate issuer.
    """
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        """
        Returns the string representation of the certificate issuer.
        """
        return self.name

class Project(models.Model):
    """
    Represents a project.
    """
    name = models.CharField(max_length=200)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        """
        Returns the string representation of the project.

        Returns:
            str: The name of the project.
        """
        return self.name
