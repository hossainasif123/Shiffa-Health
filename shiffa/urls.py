from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Include URLs from the 'users' app
    path('profiles/', include('profiles.urls', namespace='profiles')),  # Include URLs from the 'profiles' app
    path('doctor/', include('doctor.urls', namespace='doctor'))
 
]

# Add static file URL configuration
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add media file URL configuration (important for development)
if settings.DEBUG:  # Ensure this is only active in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
