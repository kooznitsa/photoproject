from django.urls import path

from . import views

app_name = 'tags'

urlpatterns = [
    path('', views.upload, name='upload'),
]
