from math import prod
from traceback import print_tb
from django.shortcuts import get_object_or_404, render
from .models import Product, Category, ItemOptions, ExtraItemOptions
from cart.forms import CartAddProductForm
from .recommender import Recommender
from .forms import ItemOptionsForm, ExtraItemOptionsForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {'category': category, 'categories': categories, 'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # product_options = ItemOptions.objects.get()

    # item_options = ItemOptions.objects.filter(Product_name_item_options=product)
    # extra_item_options = ExtraItemOptions.objects.filter(Product_name_extra_item_options=product)

    # print("item options: ", item_options)
    # print("extra item options: ", extra_item_options)

    cart_product_form = CartAddProductForm()
    cart_product_form.fields["item_options"].queryset = ItemOptions.objects.filter(Product_name_item_options=product)
    cart_product_form.fields["extra_item_options"].queryset = ExtraItemOptions.objects.filter(Product_name_extra_item_options=product)
    # item_options_form = ItemOptionsForm()
    # extra_item_option_forms = ExtraItemOptionsForm()
    # item_options_form = get_object_or_404(ItemOptions, Product_name_item_options=product)
    # extra_item_options_form = get_object_or_404(ExtraItemOptions, Product_name_extra_item_options=product)
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request, 'shop/product/detail.html', {
        'product': product, 'cart_product_form': cart_product_form, 
        'recommended_products': recommended_products,
        # 'item_options' : item_options,
        # 'extra_item_options': extra_item_options
    })

    