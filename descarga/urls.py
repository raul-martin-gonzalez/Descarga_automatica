from django.urls import path
from . import views
urlpatterns = [
    path('', views.view_descarga, name='vista_descarga')
]
