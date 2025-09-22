# portfolio/views.py
from django.shortcuts import render
from .models import CertificateIssuer, Project, Certificate
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'portfolio/home.html')

@login_required
def project_list(request):
    projects = Project.objects.order_by('-created_at')
    return render(request, "portfolio/projects.html", {"projects": projects})

@login_required
def certificate_list(request):
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
    return render(request, 'portfolio/cv.html')  # Oder PDF-Redirect
