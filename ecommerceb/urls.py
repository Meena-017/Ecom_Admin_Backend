from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),            # existing site URLs
    path('api/', include('website.api.urls')),    # ✅ add this line for API routes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
