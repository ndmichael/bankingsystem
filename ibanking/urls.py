from django.urls import path
from .views import index, charity, contact, transfer, loadbalance, invest



urlpatterns = [
    path('', index, name="index"),
    path("charity/", charity, name="charity"),
    path("contact/", contact, name="contact"),
    path("investing/", invest, name="invest"),
    path("transfer/<str:username>", transfer, name="maketransfer"),
    path("loadbalance/", loadbalance, name="loadbalance"),
]