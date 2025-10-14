# portfolio/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Certificate, Project, CertificateIssuer, Technology

@admin.register(CertificateIssuer)
class CertificateIssuerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "issuer", "issue_date", "expiry_date", "pdf_link", "url_link")
    list_filter = ("category", "issuer")
    search_fields = ("name", "issuer__name", "category")

    def pdf_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">PDF</a>', obj.pdf_file.url)
        return "-"
    pdf_link.short_description = "PDF"

    def url_link(self, obj):
        if obj.url:
            return format_html('<a href="{}" target="_blank">Link</a>', obj.url)
        return "-"
    url_link.short_description = "URL"

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_at", "image_preview", "live_url_link", "repository_url_link")
    list_filter = ("status", "technologies")
    search_fields = ("name", "description", "technologies__name")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("technologies",)
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image"

    def live_url_link(self, obj):
        if obj.live_url:
            return format_html('<a href="{}" target="_blank">Live</a>', obj.live_url)
        return "-"
    live_url_link.short_description = "Live URL"

    def repository_url_link(self, obj):
        if obj.repository_url:
            return format_html('<a href="{}" target="_blank">Repo</a>', obj.repository_url)
        return "-"
    repository_url_link.short_description = "Repository"
