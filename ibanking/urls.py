from django.urls import path
from .views import index, charity, contact, transfer, loadbalance, invest, banking_history



urlpatterns = [
    path('', index, name="index"),
    path("charity/", charity, name="charity"),
    path("contact/", contact, name="contact"),
    path("investing/", invest, name="invest"),
    path("history/add/<str:username>/", banking_history, name="banking_history"),
    path("transfer/<str:username>", transfer, name="maketransfer"),
    path("loadbalance/", loadbalance, name="loadbalance"),
]