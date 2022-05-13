# • Present a user with an order form to fill in their data
# • Create a new Order instance with the data entered, and create an associated
# OrderItem instance for each item in the cart
# • Clear all the cart's contents and redirect the user to a success page

from itertools import product
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            print("cart: ", cart)
            cart.clear()
            # launch asynchronous task using celery
            # print("celery started")
            order_created.delay(order.id)
            # print("celery finished the task")
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
