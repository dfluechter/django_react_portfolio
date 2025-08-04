from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Portfolio App
    path('', include('portfolio.urls')),
    # Auth via Djoser
    path('auth/', include('djoser.urls')),
    path('auth/jwt/', include('djoser.urls.jwt')),  # 🔑 JWT Pfad eindeutig machen

    # Django Login/Logout (für Templates)
    #path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='portfolio/logout.html'), name='logout'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
