from django.contrib import admin
from django.urls import include, path,re_path
from config import settings
from django.conf.urls.static import static 
from django.views.static import serve
urlpatterns = [
   
    
    path('admin/', admin.site.urls),
    path('',include('blog.urls',namespace='blog'))
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)