from django.conf.urls import url, include
import vendingmachine.views as vs


urlpatterns = [
    url(r'^$', vs.index),
    url(r'addvendingmachine', vs.addvendingmachine),
    url(r'editvendingmachine', vs.editvendingmachine),
    url(r'editvendingmachine_finish', vs.editvendingmachine_finish)
]
