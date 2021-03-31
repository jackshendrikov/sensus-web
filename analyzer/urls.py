from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import my_view

urlpatterns = [
    path('', my_view, name='my-view'),
    path('home/', login_required(views.home), name='home_page'),
    path('predict/', login_required(views.prediction), name='prediction'),
]
