from django.urls import path
from .views import index, charity



urlpatterns = [
    path('', index, name="index"),
    path("charity/", charity, name="charity"),
]