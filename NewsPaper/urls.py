from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urlsnw')),
    path('articles/', include('news.urlsar')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('account/', include('allauth.urls')),
              ]
