from django.urls import path, include
from accounts import views as accountViews
from . import views

urlpatterns = [
    path('', accountViews.vendorDashboard, name='vendor'),
    path('profile/', views.vendorProfile, name='vendorProfile'),
    path('menu-builder/', views.vendorMenuBuilder, name='vendorMenuBuilder'),
    path('menu-builder/category/<int:pk>/', views.vendorMenuBuilderCategory, name='vendorMenuBuilderCategory'),

    # Cetrgory CURD
    path('menu-builder/category/add/', views.vendorMenuBuilderAddCategory, name='vendorMenuBuilderAddCategory'),
    path('menu-builder/category/edit/<int:pk>/', views.vendorMenuBuilderEditCategory, name='vendorMenuBuilderEditCategory'),
    path('menu-builder/category/delete/<int:pk>', views.vendorMenuBuilderDeleteCategory, name='vendorMenuBuilderDeleteCategory'),
]
