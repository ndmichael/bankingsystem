from django.urls import path
from .views import index, charity, contact, transfer



urlpatterns = [
    path('', index, name="index"),
    path("charity/", charity, name="charity"),
    path("contact/", contact, name="contact"),
    path("transfer/<str:username>", transfer, name="maketransfer"),
]