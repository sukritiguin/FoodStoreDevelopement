from django.urls import path
from . import views

urlpatterns = [
    path(route='', view=views.marketplace, name='marketplace'),
    path(route='<slug:vendor_slug>/', view=views.vendorDeatils, name='vendorDeatils'),
    # Add to cart iteam
    path(route='add-to-cart/<int:food_id>', view=views.addToCart, name='addToCart'),
]
