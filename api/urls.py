from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api_courses.urls',namespace='api_courses')),
    path('chat/',include('chat.urls',namespace='chat')),
    path('account/',include('account.urls',namespace='account')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
