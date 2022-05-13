from django.urls import path
from .views import index, charity, contact



urlpatterns = [
    path('', index, name="index"),
    path("charity/", charity, name="charity"),
    path("contact/", contact, name="contact"),
]