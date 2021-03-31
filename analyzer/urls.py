from django.conf.urls import url
from django.urls import path
from . import views
from .views import my_view

urlpatterns = [
    path('', my_view, name='my-view'),
    # url(r'^$', views.home, name='index'),
    url(r'^predict/', views.prediction, name='prediction'),
]
