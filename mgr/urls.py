from django.urls import path
from mgr import customer,sign_in_out,medicine,orders

urlpatterns = [
    path('customers/', customer.dispatcher),
    path('medicine/',medicine.dispatcher),
    path('orders/',orders.dispatcher),
    path('signin/',sign_in_out.signin),
    path('signout/',sign_in_out.signout),
] 