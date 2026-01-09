# portfolio/tests/test_admin.py
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio.admin import CertificateAdmin, ProjectAdmin
from portfolio.models import Certificate, Project
from tests.unit.factories import CertificateFactory, ProjectFactory


class AdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()


class CertificateAdminTest(AdminTestCase):
    def test_pdf_link_with_file(self):
        cert = CertificateFactory(pdf_file=SimpleUploadedFile("test.pdf", b"content"))
        admin = CertificateAdmin(Certificate, self.site)
        self.assertEqual(
            admin.pdf_link(cert),
            f'<a href="{cert.pdf_file.url}" target="_blank">PDF</a>',
        )

    def test_pdf_link_without_file(self):
        # Nutze None oder leeren String, je nach Model-Definition
        cert = CertificateFactory(pdf_file=None)
        admin = CertificateAdmin(Certificate, self.site)
        self.assertEqual(admin.pdf_link(cert), "-")

    def test_url_link_with_url(self):
        # Das Model Feld heißt 'url', die Admin Methode 'url_link'
        cert = CertificateFactory(url="http://example.com")
        admin = CertificateAdmin(Certificate, self.site)
        self.assertEqual(
            admin.url_link(cert), f'<a href="{cert.url}" target="_blank">Link</a>'
        )

    def test_certificate_admin_url_empty(self):
        """Testet das '-' Label, wenn keine URL vorhanden ist (Line 26/60)."""
        cert = CertificateFactory(url="")
        admin = CertificateAdmin(Certificate, self.site)
        self.assertEqual(admin.url_link(cert), "-")

    def test_project_admin_image_none(self):
        """Testet 'No Image' Label (Line 46-48)."""
        project = ProjectFactory(image=None)
        admin = ProjectAdmin(Project, self.site)
        self.assertEqual(admin.image_preview(project), "No Image")


class ProjectAdminTest(AdminTestCase):
    def test_live_url_link(self):
        # Case: URL vorhanden
        project = ProjectFactory(live_url="http://example.com")
        admin = ProjectAdmin(Project, self.site)
        self.assertEqual(
            admin.live_url_link(project),
            f'<a href="{project.live_url}" target="_blank">Live</a>',
        )

        # Case: URL fehlt (deckt Missing Line ab)
        project_empty = ProjectFactory(live_url="")
        self.assertEqual(admin.live_url_link(project_empty), "-")

    def test_repository_url_link(self):
        # Case: Repo vorhanden
        project = ProjectFactory(repository_url="http://github.com")
        admin = ProjectAdmin(Project, self.site)
        self.assertEqual(
            admin.repository_url_link(project),
            f'<a href="{project.repository_url}" target="_blank">Repo</a>',
        )

        # Case: Repo fehlt (deckt Missing Line ab)
        project_empty = ProjectFactory(repository_url="")
        self.assertEqual(admin.repository_url_link(project_empty), "-")

    def test_image_preview(self):
        admin = ProjectAdmin(Project, self.site)

        # Case: Kein Bild (deckt Missing Line ab)
        project_no_img = ProjectFactory(image=None)
        self.assertEqual(admin.image_preview(project_no_img), "No Image")

    def test_image_preview_with_file(self):
    # Erstelle ein minimales 1x1 Pixel GIF im Speicher
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        img_file = SimpleUploadedFile("test.gif", small_gif, content_type="image/gif")
        project = ProjectFactory(image=img_file)
        admin = ProjectAdmin(Project, self.site)

        preview_html = admin.image_preview(project)
        assert '<img src=' in preview_html
        assert project.image.url in preview_html