from decimal import Decimal
from email.policy import default
from django.conf import settings
from shop.models import Product, ItemOptions, ExtraItemOptions
from coupons.models import Coupon

class Cart(object):
    def __init__(self, request):
        """Intializing th Cart

        Args:
            request (dict): cart items
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id') # coupon

    def add(self, product, quantity=1, override_quantity=False, override_item_options=False, override_extra_item_options=False, item_options=None, extra_item_options=None):
        """Add products to the cart or update the quantity

        Args:
            product (dict): the name of the product
            quantity (int, optional): item_description_. Defaults to 1.
            override_quantity (bool, optional): item_description_. Defaults to False.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price), }
            # 'item_options': item_options, 'extra_item_options': extra_item_options
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        # if override_item_options:
        #     self.cart[product_id]['item_options'] = item_options
        # else:
        #     pass
        # if override_extra_item_options:
        #     self.cart[product_id]['extra_item_options'] = extra_item_options
        # else:
        #     pass
        self.save()

    def save(self):
        # mark the session "modified to make sure it saved"
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart.

        Args:
            product (dict): removed product details from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """Iterate over the items in the cart and get the product from the database
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            # try:
            #     item['item_options'] = Decimal(item['item_options'])
            #     item['extra_item_options'] = Decimal(item['extra_item_options'])
            # except:
            #     item['item_options'] = Decimal(0)
            #     item['extra_item_options'] = Decimal(0)

            item['price'] = Decimal(item['price'])

            item['total_price'] = item['price'] * item['quantity'] 
            # +  item['item_options'] + item['extra_item_options']
            yield item

    def __len__(self):
        """count all the items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """get total price of products in the cart
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Removing the cart from the session (empty the cart)
        """
        del self.session[settings.CART_SESSION_ID] # release the cart session
        self.save()
    
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()