from django.test import TestCase
from portfolio.factories import (
    CertificateFactory,
    CertificateIssuerFactory,
    ProjectFactory,
)


class CertificateModelTest(TestCase):
    def test_str_returns_certificate_name(self):
        cert = CertificateFactory(name="Python Basics")
        self.assertEqual(str(cert), "Python Basics")

    def test_certificate_has_valid_upload_path(self):
        cert = CertificateFactory()
        expected_path = f"certificates/{cert.issuer.name.lower().replace(' ', '-')}/{cert.pdf_file.name.split('/')[-1]}"
        self.assertEqual(cert.pdf_file.name, expected_path)
        self.assertTrue(cert.pdf_file.name.endswith(".pdf"))


class CertificateIssuerModelTest(TestCase):
    def test_str_returns_issuer_name(self):
        issuer = CertificateIssuerFactory(name="OpenAI Academy")
        self.assertEqual(str(issuer), "OpenAI Academy")


class ProjectModelTest(TestCase):
    def test_str_returns_project_name(self):
        project = ProjectFactory(name="My Fancy Portfolio")
        self.assertEqual(str(project), "My Fancy Portfolio")

    def test_project_url_is_valid(self):
        project = ProjectFactory(url="https://example.com")
        self.assertTrue(project.url.startswith("https://"))