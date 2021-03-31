from django.urls import path
from . import views
from .views import my_view

urlpatterns = [
    path('', my_view, name='my-view'),
    path('home/', views.home, name='home_page'),
    path('predict/', views.prediction, name='prediction'),
]
