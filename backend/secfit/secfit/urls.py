from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from secfit import views
urlpatterns = [
    path("", views.api_root),
    path("admin/", admin.site.urls),
    path("", include("workouts.urls")),
    path("", include("suggested_workouts.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
