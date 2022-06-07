from django.urls import path
from .views import (
    profile, admin, all_users, all_transfers, 
    update_users, register, change_pin, change_password
)



urlpatterns = [
    path("profile/<str:username>", profile, name="userprofile"),
    path("users/admin", admin, name="adminpage"),
    path("users/all", all_users, name="all_users"),
    path("all/transfers/", all_transfers, name="all_transfer"),
    path("users/register/", register, name="register"),
    path("users/update/<str:username>", update_users, name="update_user"),
    path("users/changepin/", change_pin, name="change_pin"),
    path("profile/changepassword/<int:id>/", change_password, name="change_password"),
]