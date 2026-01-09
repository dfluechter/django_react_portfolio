import pytest

@pytest.mark.security
def test_admin_panel_not_accessible_for_public(client):
    url = '/admin/'
    response = client.get(url)
    # Erwartet Redirect zum Login oder 403
    assert response.status_code in [302, 403]