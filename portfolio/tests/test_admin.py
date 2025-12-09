# portfolio/tests/test_admin.py
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio.admin import CertificateAdmin, ProjectAdmin, CertificateIssuerAdmin
from portfolio.models import Certificate, Project, CertificateIssuer
from .factories import CertificateFactory, ProjectFactory

class MockRequest:
    pass

class MockSuperUser:
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()

class AdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()

class CertificateAdminTest(AdminTestCase):
    def test_pdf_link_with_file(self):
        cert = CertificateFactory(pdf_file=SimpleUploadedFile("test.pdf", b"content"))
        admin = CertificateAdmin(Certificate, self.site)
        self.assertEqual(admin.pdf_link(cert), f'<a href="{cert.pdf_file.url}" target="_blank">PDF</a>')

    def test_pdf_link_without_file(self):
        cert = CertificateFactory(pdf_file=None)
        admin = CertificateAdmin(Certificate, self.site)
        self.assertEqual(admin.pdf_link(cert), '-')

    def test_url_link_with_url(self):
        cert = CertificateFactory(url="http://example.com")
        admin = CertificateAdmin(Certificate, self.site)
        self.assertEqual(admin.url_link(cert), f'<a href="{cert.url}" target="_blank">Link</a>')

    def test_url_link_without_url(self):
        cert = CertificateFactory(url="")
        admin = CertificateAdmin(Certificate, self.site)
        self.assertEqual(admin.url_link(cert), '-')

class ProjectAdminTest(AdminTestCase):
    def test_url_link(self):
        project = ProjectFactory(url="http://example.com")
        admin = ProjectAdmin(Project, self.site)
        self.assertEqual(admin.url_link(project), f'<a href="{project.url}" target="_blank">Link</a>')
