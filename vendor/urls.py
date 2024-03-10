from django.urls import path, include
from accounts import views as accountViews
from . import views

urlpatterns = [
    path('', accountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vendorProfile, name='vendorProfile'),
]
