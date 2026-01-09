import os
import uuid
import magic
from django.db import models, transaction, IntegrityError
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def certificate_upload_path(instance, filename):
    # Für Migration 0002
    return f'certificates/{filename}'

def certificate_pdf_upload_path(instance, filename):
    # Für Migration 0006
    return f'certificates/{filename}'

def project_image_upload_path(instance, filename):
    # Für Migration 0005 (Das war der letzte Fehler!)
    return f'projects/{filename}'

def validate_pdf_mimetype(file):
    # Für Migration 0006
    try:
        mime_type = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)
        if mime_type != 'application/pdf':
            raise ValidationError('Unsupported file type.')
    except Exception:
        # Fallback, falls Datei leer oder magic nicht verfügbar
        file.seek(0)

def validate_mime_type_pdf(file):
    """
    Validates that the uploaded file is actually a PDF by inspecting its header (Magic Bytes).
    Prevents Polyglot attacks where malicious code is hidden in files with.pdf extension.
    """
    initial_pos = file.tell()
    file.seek(0)
    # Read the first 2048 bytes to determine MIME type securely
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(initial_pos)
    
    if mime_type!= 'application/pdf':
        raise ValidationError(
            _('File is not a valid PDF. Detected type: %(type)s'), 
            params={'type': mime_type}
        )

def generate_unique_slug(instance, source_value, slug_field_name='slug'):
    """
    Generates a unique slug by appending a counter if the slug already exists.
    Handles updates correctly by excluding the current instance PK.
    """
    original_slug = slugify(source_value)
    unique_slug = original_slug
    num = 1
    ModelClass = instance.__class__
    
    # Check for collisions excluding the current instance (idempotency check)
    while ModelClass.objects.filter(**{slug_field_name: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f'{original_slug}-{num}'
        num += 1
    return unique_slug

def secure_certificate_path(instance, filename):
    """
    Generates a secure, immutable path using the issuer's ID and a UUID filename.
    Structure: certificates/{issuer_id}/{uuid}.pdf
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    # Use issuer_id (FK) directly to avoid N+1 Select query
    issuer_id = getattr(instance, 'issuer_id', 'unknown')
    return f"certificates/{issuer_id}/{filename}"

def secure_project_image_path(instance, filename):
    """
    Generates a secure path using UUID to prevent Directory Traversal and file overwrites.
    Structure: projects/images/{uuid}.{ext}
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"projects/images/{filename}"

class CertificateIssuer(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Certificate(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    
    # Changed to PROTECT to prevent accidental deletion of issuer triggering mass certificate deletion
    issuer = models.ForeignKey(
        "CertificateIssuer", 
        on_delete=models.PROTECT,
        related_name='certificates'
    )
    
    # Added Validators (Extension & MIME-Type) and Secure Path
    pdf_file = models.FileField(
        upload_to=secure_certificate_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_mime_type_pdf
        ]
    )
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Using robust slug generation loop
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    # Modern TextChoices instead of Tuple
    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", _("In Progress")
        COMPLETED = "completed", _("Completed")
        ARCHIVED = "archived", _("Archived")

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    # Removed null=True to avoid ambiguous "empty" states
    title = models.CharField(max_length=100, blank=True, default="")
    
    description = models.TextField()
    
    image = models.ImageField(
        upload_to=secure_project_image_path, 
        blank=True, 
        null=True
    )
    
    live_url = models.URLField(blank=True)
    repository_url = models.URLField(blank=True)
    
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.IN_PROGRESS
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Added related_name for cleaner reverse access (project.technologies.all() / tech.projects.all())
    technologies = models.ManyToManyField(
        Technology, 
        blank=True,
        related_name="projects"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)
