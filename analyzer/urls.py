from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import upload

urlpatterns = [
    path('', upload, name='upload'),
    path('home/', login_required(views.home), name='home_page'),
    path('predict/', login_required(views.prediction), name='prediction'),
]
