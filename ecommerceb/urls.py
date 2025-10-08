# from django.contrib import admin
# from django.urls import include, path
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
    
#     # Website frontend routes
#     path('', include(('website.urls', 'website'), namespace='website')),
    
#     # API routes with unique namespace
#     path('api/', include(('website.api.urls', 'website_api'), namespace='website_api')),
# ]

# # Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),            # existing site URLs
    path('api/', include('website.api.urls')),    # ✅ add this line for API routes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
