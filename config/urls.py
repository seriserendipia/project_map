from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('map_app/', include('map_app.urls', namespace='map_app')),
    path('', include('map_app.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

# 添加静态文件服务
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 