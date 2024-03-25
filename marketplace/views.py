from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch

from .context_processors import get_cart_counter
from vendor.models import Vendor
from menu.models import Category, FoodItem
from .models import Cart

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
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user = request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request=request, template_name='marketplace/vendorDeatils.html', context=context)

# def addToCart(request, food_id):
    
#     if request.user.is_authenticated:
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             try:
#                 fooditem = FoodItem.objects.get(id=food_id)
#                 # Check if user is already added the food item to cart or not
#                 try:
#                     cart = Cart.objects.get(user=request.user, fooditem=fooditem)
#                     # Cart is existing, So increase the quantity
#                     cart.quantity += 1
#                     cart.save()
#                     return JsonResponse({
#                         'status': 'success',
#                         'message': 'Increased the card quantity.',
#                         'cart_counter': get_cart_counter(),
#                     })
#                 except:
#                     cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
#                     cart.save()
#                     return JsonResponse({
#                         'status': 'success',
#                         'message': 'Fooditem added to the cart successfully.'
#                     })
#             except:
#                 return JsonResponse({
#                     'status': 'Failed',
#                     'message': 'Food item does not exist'
#                 })
#         return JsonResponse({
#         'status': 'Failed',
#         'message': 'Invalid Request'
#     })
    
#     return JsonResponse({
#         'status': 'Failed',
#         'message': 'Please login to continue.'
#     })


def addToCart(request, food_id):
    
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if user has already added the food item to cart or not
                try:
                    # Retrieve the cart item based on the fooditem and user
                    cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Cart exists, so increase the quantity
                    cart.quantity += 1
                    cart.save()
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Increased the cart quantity.',
                        'cart_counter': get_cart_counter(request),
                        'quantity': cart.quantity,
                    })
                except Cart.DoesNotExist:
                    # If the cart item does not exist, create a new one
                    cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Food item added to the cart successfully.',
                        'cart_counter': get_cart_counter(request),
                        'quantity': cart.quantity,
                    })
            except FoodItem.DoesNotExist:
                return JsonResponse({
                    'status': 'Failed',
                    'message': 'Food item does not exist'
                })
        return JsonResponse({
            'status': 'Failed',
            'message': 'Invalid Request'
        })
    
    return JsonResponse({
        'status': 'Failed',
        'message': 'Please log in to continue.'
    })
