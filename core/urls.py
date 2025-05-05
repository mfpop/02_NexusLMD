from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import RedirectView


# Function for redirecting root URL
def redirect_to_home(request):
    return redirect('auth_home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("about/", include("apps.about.urls")),
    path("contact/", include("apps.contact.urls")),
    path("activities/", include("apps.activities.urls")),
    path("chat/", include("apps.chat.urls")),
    path("", include("apps.home.urls")),
    path("metrics/", include("apps.metrics.urls")),
    path("news/", include("apps.news.urls")),
    path("production/", include("apps.production.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    
    # Authentication app URLs
    path('auth/', include('apps.authenticate.urls')),
    path(
        'accounts/profile/', 
        RedirectView.as_view(url='/auth/profile/', permanent=False), 
        name='default_profile_redirect'
    ),
    
    # Root URL redirects to home
    path('', lambda request: redirect('home:index'), name='root'),
]

# Add static and media files URLs if in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
