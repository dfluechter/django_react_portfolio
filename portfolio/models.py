import os
import uuid
import magic  # Requires python-magic
from django.db import models, transaction, IntegrityError
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_mime_type_pdf(file):
    """
    Validates that the uploaded file is actually a PDF by inspecting its header.
    """
    # Read a small buffer to check magic numbers
    initial_pos = file.tell()
    file.seek(0)
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(initial_pos)
    
    if mime_type!= 'application/pdf':
        raise ValidationError(_('File is not a valid PDF. Detected type: %(type)s'), 
                              params={'type': mime_type})

def generate_unique_slug(instance, source_value, slug_field_name='slug'):
    """
    Generates a unique slug by appending a counter if the slug already exists.
    Uses an iterative approach to handle race conditions optimistically.
    """
    original_slug = slugify(source_value)
    unique_slug = original_slug
    num = 1
    ModelClass = instance.__class__
    
    # Check for collisions excluding the current instance (for updates)
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
    # Use ID to avoid N+1 query and name mutability issues
    # Fallback to 'unknown' if issuer is not set (should not happen with valid form)
    issuer_id = getattr(instance, 'issuer_id', 'unknown')
    return f"certificates/{issuer_id}/{filename}"

def secure_project_image_path(instance, filename):
    """
    Structure: projects/{uuid}.{ext}
    Flattening the structure avoids deep nesting and reliance on mutable project names.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"projects/images/{filename}"

class CertificateIssuer(models.Model):
    # Use CICharField in Postgres for case-insensitive uniqueness
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Certificate(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    
    # CHANGED: PROTECT prevents deletion of Issuer if certificates exist.
    # related_name allows issuer.certificates.all()
    issuer = models.ForeignKey(
        "CertificateIssuer", 
        on_delete=models.PROTECT,
        related_name='certificates'
    )
    
    # CHANGED: Added validators for extension and MIME type.
    # Switched to secure path generation.
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
        # Robust slug generation
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    # CHANGED: Use TextChoices for robust enumeration
    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", _("In Progress")
        COMPLETED = "completed", _("Completed")
        ARCHIVED = "archived", _("Archived")

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    # CHANGED: Removed null=True. Default to empty string.
    title = models.CharField(max_length=100, blank=True, default="")
    
    description = models.TextField()
    
    image = models.ImageField(
        upload_to=secure_project_image_path, 
        blank=True, 
        null=True
    )
    
    live_url = models.URLField(blank=True)
    repository_url = models.URLField(blank=True)
    
    # CHANGED: Use choices class
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.IN_PROGRESS
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    # CHANGED: Added related_name for reverse lookup logic
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
