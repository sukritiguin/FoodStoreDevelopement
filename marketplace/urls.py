from django.urls import path
from . import views

urlpatterns = [
    path(route='', view=views.marketplace, name='marketplace'),
    path(route='<slug:vendor_slug>/', view=views.vendorDeatils, name='vendorDeatils'),
]
