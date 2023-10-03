from django.urls import path
from app01 import views

urlpatterns = [
    path('index01/', views.Index), 
    path('index02/', views.Index2),
    path('listcustomers/', views.listcustomers),
    path('addcustomers/',views.CustomersAdd),
    path('showcustomers/',views.ShowCustomers),
    path('deletecusotmers/',views.deleteCustomers)
] 