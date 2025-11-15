import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRedirects
from .factories import UserFactory, ProjectFactory, CertificateFactory, CertificateIssuerFactory

@pytest.mark.django_db
def test_home_view_authenticated(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'portfolio/home.html')

@pytest.mark.django_db
def test_home_view_unauthenticated(client):
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 302
    assertRedirects(response, f'/login/?next={url}')

@pytest.mark.django_db
def test_cv_view_authenticated(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse('cv')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'portfolio/cv.html')

@pytest.mark.django_db
def test_cv_view_unauthenticated(client):
    url = reverse('cv')
    response = client.get(url)
    assert response.status_code == 302
    assertRedirects(response, f'/login/?next={url}')

@pytest.mark.django_db
def test_certificate_list_view_authenticated_no_issuer(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse('certificate_list')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'portfolio/certificates.html')
    assert 'certificates' in response.context
    assert len(response.context['certificates']) == 0

@pytest.mark.django_db
def test_certificate_list_view_authenticated_with_issuer(client):
    user = UserFactory()
    client.force_login(user)
    issuer = CertificateIssuerFactory()
    CertificateFactory.create_batch(3, issuer=issuer)
    CertificateFactory.create_batch(2) # other certificates
    url = reverse('certificate_list')
    response = client.get(url, {'issuer': issuer.id})
    assert response.status_code == 200
    assertTemplateUsed(response, 'portfolio/certificates.html')
    assert 'certificates' in response.context
    assert len(response.context['certificates']) == 3
    assert response.context['selected_issuer'] == issuer.id

@pytest.mark.django_db
def test_certificate_list_view_with_invalid_issuer_id(client):
    user = UserFactory()
    client.force_login(user)
    url = reverse('certificate_list')
    response = client.get(url, {'issuer': 'invalid'})
    assert response.status_code == 200
    assertTemplateUsed(response, 'portfolio/certificates.html')
    assert 'certificates' in response.context
    assert len(response.context['certificates']) == 0
    assert response.context['selected_issuer'] is None

@pytest.mark.django_db
def test_certificate_list_view_unauthenticated(client):
    url = reverse('certificate_list')
    response = client.get(url)
    assert response.status_code == 302
    assertRedirects(response, f'/login/?next={url}')

@pytest.mark.django_db
def test_project_list_view_authenticated(client):
    user = UserFactory()
    client.force_login(user)
    ProjectFactory.create_batch(5)
    url = reverse('project_list')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'portfolio/projects.html')
    assert 'projects' in response.context
    assert len(response.context['projects']) == 5

@pytest.mark.django_db
def test_project_list_view_unauthenticated(client):
    url = reverse('project_list')
    response = client.get(url)
    assert response.status_code == 302
    assertRedirects(response, f'/login/?next={url}')
