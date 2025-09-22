# portfolio/admin.py
"""
Admin configurations for the portfolio app.
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from .models import Certificate, Project, CertificateIssuer

@admin.register(CertificateIssuer)
class CertificateIssuerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CertificateIssuer model.
    """
    list_display = ("name",)
    search_fields = ("name",)
    
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Certificate model.
    """
    list_display = ("name", "category", "issuer", "issue_date", "expiry_date", "pdf_link", "url_link")
    list_filter = ("category", "issuer")
    search_fields = ("name", "issuer", "category")

    def pdf_link(self, obj):
        """
        Returns an HTML link to the certificate's PDF file.

        Args:
            obj: The Certificate instance.

        Returns:
            str: An HTML link to the PDF file, or "-" if no file is available.
        """
        if obj.pdf_file:
            return f'<a href="{obj.pdf_file.url}" target="_blank">PDF</a>'
        return "-"
    pdf_link.allow_tags = True
    pdf_link.short_description = "PDF"

    def url_link(self, obj):
        """
        Returns an HTML link to the certificate's URL.

        Args:
            obj: The Certificate instance.

        Returns:
            str: An HTML link to the URL, or "-" if no URL is available.
        """
        if obj.url:
            return f'<a href="{obj.url}" target="_blank">Link</a>'
        return "-"
    url_link.allow_tags = True
    url_link.short_description = "URL"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Project model.
    """
    list_display = ("name", "created_at", "url_link")
    search_fields = ("name", "description")
    ordering = ("-created_at",)

    def url_link(self, obj):
        """
        Returns an HTML link to the project's URL.

        Args:
            obj: The Project instance.

        Returns:
            str: An HTML link to the project's URL.
        """
        return f'<a href="{obj.url}" target="_blank">Link</a>'
    url_link.allow_tags = True
    url_link.short_description = "URL"
