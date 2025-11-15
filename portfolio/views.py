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
        try:
            issuer_id_int = int(issuer_id)
            certificates = Certificate.objects.filter(issuer__id=issuer_id_int)
            selected_issuer = issuer_id_int
        except (ValueError, TypeError):
            certificates = Certificate.objects.none()
            selected_issuer = None
    else:
        certificates = Certificate.objects.none()
        selected_issuer = None

    return render(request, "portfolio/certificates.html", {
        "certificates": certificates,
        "issuers": issuers,
        "selected_issuer": selected_issuer,})

@login_required
def cv(request):
    return render(request, 'portfolio/cv.html')
