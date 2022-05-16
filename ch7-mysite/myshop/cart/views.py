from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm
# from myshop.coupons.views import coupon_apply
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

from shop.recommender import Recommender

@require_POST
def cart_add(request, product_id):
    """This is the view for adding products to the cart or updating quantities for existing
    products. You use the require_POST decorator to allow only POST requests. The
    view receives the product ID as a parameter. You retrieve the Product instance
    with the given ID and validate CartAddProductForm. If the form is valid, you either
    add or update the product in the cart. The view redirects to the cart_detail URL,
    which will display the contents of the cart.

    Args:
        request (dict): request
        product_id (id): product_id

    Returns:
        cart_Detail: redirect to product_url
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
        return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """The cart_remove view receives the product ID as a parameter. You use the
    require_POST decorator to allow only POST requests. You retrieve the Product
    instance with the given ID and remove the product from the cart. Then, you redirect
    the user to the cart_detail URL.

    Args:
        request (dict): request
        product_id (id): product_id

    Returns:
        cart_Detail: redirect to product_url
    """
    cart = Cart(request)
    product= get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """You create an instance of CartAddProductForm for each item in the cart to allow
    changing product quantities. You initialize the form with the current item quantity
    and set the override field to True so that when you submit the form to the cart_
    add view, the current quantity is replaced with the new one.

    Args:
        request (dict): request

    Returns:
        dict: cart
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial = {
            'quantity': item['quantity'],
            'override': True
        })
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    print("cart_products: ", cart_products)
    recommended_products = r.suggest_products_for(cart_products, max_results=4)
    print("recommended products: ", recommended_products)
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form, 
        'recommended_products': recommended_products
    })

    
    

