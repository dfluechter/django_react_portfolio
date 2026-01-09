import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_status_code(admin_client):  # admin_client ist automatisch eingeloggt
    url = reverse("home")
    response = admin_client.get(url)
    assert response.status_code == 200
