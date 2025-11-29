# Copilot Instructions for Django Portfolio

## Project Overview
A Django 5.2 portfolio application with Tailwind CSS frontend, JWT authentication (Djoser), and responsive design (dark mode, burger menu). Demonstrates Django patterns for media management, authentication, and template-driven UI.

## Architecture

### Three-Tier Structure
- **Backend**: Django views + REST API (Djoser/DRF)
- **Frontend**: Server-rendered templates (Tailwind + Alpine.js)
- **Data**: SQLite (dev), PostgreSQL (prod via `dj-database-url`)

### Key Components
- **`portfolio/models.py`**: Four core models (Certificate, CertificateIssuer, Project, Technology) with auto-slug generation and custom upload paths
- **`portfolio/views.py`**: Login-required views with context filtering (e.g., certificate filtering by issuer ID via GET param)
- **`config/settings.py`**: Environment-based config (dev/prod via `DJANGO_ENV` variable)
- **`portfolio/templates/`**: Server-rendered pages (no React, despite project name)

### Data Relationships
```
Project ──M2M─→ Technology
Certificate ──FK─→ CertificateIssuer
```

## Critical Workflows

### Running Locally
```bash
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\activate (Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Testing
- Framework: pytest + pytest-django + factory_boy
- Config: `pytest.ini` specifies `DJANGO_SETTINGS_MODULE = config.settings`
- Run: `pytest` or `pytest portfolio/tests/test_*.py` (verbose, short traceback, warnings disabled)
- Test files use `@pytest.mark.django_db` decorator for database access
- Factory pattern: `UserFactory`, `ProjectFactory`, etc. in `portfolio/tests/factories.py`

### Deployment
- Render.yaml orchestrates build steps (collectstatic, migrate)
- Environment: `DJANGO_ENV=prod` triggers `settings_prod.py` import
- Database: External PostgreSQL connection via `DATABASE_URL` env var (Netlify/Supabase)
- Media files: `/media/` directory (served in dev via `django.conf.urls.static`)

### Certificate Import
Custom management command: `python manage.py import_certificates`
- Scans `media/certificates/<issuer_folder>/` for PDFs
- Auto-creates `CertificateIssuer` from folder names (kebab-case → Title Case)
- Skips duplicates (checks name + issuer combination)

## Project-Specific Patterns

### Auto-Slug Generation
Models use `save()` override to auto-generate slugs if blank:
```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.name)
    super().save(*args, **kwargs)
```
See: `Technology`, `Project` models.

### Upload Path Functions
Use custom functions for organized media storage by slug:
```python
def certificate_upload_path(instance, filename):
    issuer_slug = slugify(instance.issuer.name)
    return f"certificates/{issuer_slug}/{filename}"
```
See: `certificate_upload_path`, `project_image_upload_path` in `models.py`.

### Query-Parameter Filtering
Views filter querysets via GET params (e.g., `certificate_list?issuer=1`):
```python
issuer_id = request.GET.get("issuer")
if issuer_id:
    try:
        issuer_id_int = int(issuer_id)
        certificates = Certificate.objects.filter(issuer__id=issuer_id_int)
    except (ValueError, TypeError):
        certificates = Certificate.objects.none()
```
This pattern handles invalid input gracefully (returns empty queryset).

### Admin Customization
`admin.py` uses `format_html()` for clickable links to PDFs/URLs:
```python
def pdf_link(self, obj):
    if obj.pdf_file:
        return format_html('<a href="{}" target="_blank">PDF</a>', obj.pdf_file.url)
    return "-"
```

## Authentication & Authorization
- **Framework**: Django session auth + Djoser JWT endpoints
- **Decorators**: `@login_required` on all views (redirects to `/login/`)
- **Endpoints**: 
  - `/auth/login/` (Djoser)
  - `/auth/token/` (JWT)
  - `/auth/logout/` (Django)
- **DRF Config**: Token + JWT auth, `IsAuthenticated` permission class by default

## Development Configuration

### Key Settings
- **Language**: German (LANGUAGE_CODE = 'de-de')
- **Timezone**: Europe/Berlin
- **Static Files**: Served from `staticfiles/` (production) or automatically (dev)
- **CORS**: All origins allowed in dev (`CORS_ALLOW_ALL_ORIGINS = True`)
- **Database**: SQLite in dev (db.sqlite3), PostgreSQL in prod

### Environment Variables (Production)
- `DJANGO_ENV=prod` → loads `settings_prod.py`
- `DATABASE_URL` → PostgreSQL connection string (required for prod)
- `CREATE_SUPERUSER` → Set for automated superuser creation in deployment

## Testing Strategy
- Use factories for all test data (`ProjectFactory.create_batch(5)`)
- Test authenticated vs. unauthenticated paths (redirects to login)
- Use `assertRedirects()` for 302 responses, `assertTemplateUsed()` for template validation
- Always decorate database tests with `@pytest.mark.django_db`

## Common Gotchas
1. **Slug fields are optional** (`blank=True`) but auto-filled in `save()`—safe to create without specifying
2. **Certificate import is case-sensitive** for extensions (checks `.lower().endswith(".pdf")`)
3. **Invalid issuer ID in GET param** → returns empty certificates, not error (by design)
4. **Login required** applies to all views—no public endpoints currently
5. **Media root differs by OS** → use `os.path.join()` not hardcoded paths
