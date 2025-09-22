# portfolio/views.py
"""
Views for the portfolio app.
"""
from django.shortcuts import render
from .models import CertificateIssuer, Project, Certificate
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """
    Renders the home page.

    Args:
        request: The HTTP request.

    Returns:
        The rendered home page.
    """
    return render(request, 'portfolio/home.html')

@login_required
def project_list(request):
    """
    Renders the project list page.

    Args:
        request: The HTTP request.

    Returns:
        The rendered project list page.
    """
    projects = Project.objects.order_by('-created_at')
    return render(request, "portfolio/projects.html", {"projects": projects})

@login_required
def certificate_list(request):
    """
    Renders the certificate list page.

    Args:
        request: The HTTP request.

    Returns:
        The rendered certificate list page.
    """
    issuer_id = request.GET.get("issuer")
    issuers = CertificateIssuer.objects.all().order_by("name")

    if issuer_id:
        certificates = Certificate.objects.filter(issuer__id=issuer_id)
    else:
        certificates = Certificate.objects.none()

    return render(request, "portfolio/certificates.html", {
        "certificates": certificates,
        "issuers": issuers,
        "selected_issuer": int(issuer_id) if issuer_id else None,})

@login_required
def cv(request):
    """
    Renders the CV page.

    Args:
        request: The HTTP request.

    Returns:
        The rendered CV page.
    """
    return render(request, 'portfolio/cv.html')
