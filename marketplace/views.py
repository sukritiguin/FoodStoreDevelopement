from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch

from vendor.models import Vendor
from menu.models import Category, FoodItem

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request=request, template_name='marketplace/listings.html', context=context)

def vendorDeatils(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    # Applying reverse lookup - using prefech related & related name in the FoodItem model
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available = True)
        )
    )
    context = {
        'vendor': vendor,
        'categories': categories,
    }
    return render(request=request, template_name='marketplace/vendorDeatils.html', context=context)
