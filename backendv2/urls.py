# backend/simplemodel/urls.py
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

urlpatterns = [
    url(r'^api/v1/', include('camp.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/base-auth/', include("rest_framework.urls")),
    url(r'^api/v1/auth/', include("djoser.urls")),
    url(r'^api/v1/auth_token/', include("djoser.urls.authtoken"))]
