import pytest
from django.urls import reverse, resolve
from portfolio import views

@pytest.mark.django_db
def test_home_url():
    url = reverse('home')
    assert resolve(url).func == views.home

@pytest.mark.django_db
def test_project_list_url():
    url = reverse('project_list')
    assert resolve(url).func == views.project_list

@pytest.mark.django_db
def test_certificate_list_url():
    url = reverse('certificate_list')
    assert resolve(url).func == views.certificate_list

@pytest.mark.django_db
def test_cv_url():
    url = reverse('cv')
    assert resolve(url).func == views.cv
