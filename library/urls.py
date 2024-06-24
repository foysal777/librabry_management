
from django.contrib import admin
from django.urls import path,include
from account_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , views.home , name= 'home') ,
    path('account/' , include('account_app.urls')) ,
    path('account/' , include('transaction.urls')) ,
    
    
]
if settings.DEBUG:urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)