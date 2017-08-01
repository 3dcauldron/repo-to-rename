from django.conf.urls import url, include
import gcode_access.views as vs

urlpatterns = [
    url(r'^$', vs.index)
]