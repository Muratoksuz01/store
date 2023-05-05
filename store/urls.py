from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
path('', views.store, name="store"),
path('cart/', views.cart, name="cart"),
path('checkout/', views.checkout, name="checkout"),  
path('update_item/', views.updateItem, name="updateItem"),   
path('process_order/', views.processorder, name="process_order"),   


]
