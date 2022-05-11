from django.urls import path
from .views import profile, admin, all_users, all_transfers



urlpatterns = [
    path("profile/<str:username>", profile, name="userprofile"),
    path("users/admin", admin, name="adminpage"),
    path("users/all", all_users, name="all_users"),
    path("transfer/all", all_transfers, name="all_transfer"),
]