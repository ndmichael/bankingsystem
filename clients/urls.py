from django.urls import path
from .views import profile, admin



urlpatterns = [
    path("profile/<str:username>", profile, name="userprofile"),
    path("users/admin", admin, name="adminpage"),
]