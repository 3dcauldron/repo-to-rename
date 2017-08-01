from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from userapi import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^djangojs/', include('djangojs.urls')),
    url(r'^gcode_access/', include('gcode_access.urls')),
    url(r'^vendingmachine/', include('vendingmachine.urls')),
    url(r'^users/', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^swaggerapp/', include('swaggerapp.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', TemplateView.as_view(template_name='exampleapp/itworks.html'), name='home'),
]
