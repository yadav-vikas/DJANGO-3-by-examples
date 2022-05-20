from django import forms
from django.utils.translation import gettext_lazy as _
from shop.models import ItemOptions, ExtraItemOptions, Product
from shop.forms import ItemOptionsForm, ExtraItemOptionsForm

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    """quantity: This allows the user to select a quantity between one and 20. You
    use a TypedChoiceField field with coerce=int to convert the input into
    an integer.

    • override: This allows you to indicate whether the quantity has to be added
    to any existing quantity in the cart for this product (False), or whether the
    existing quantity has to be overridden with the given quantity (True). You
    use a HiddenInput widget for this field, since you don't want to display it
    to the user.

    Args:
        forms (list): quantity if products and override the quantity
    """


    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=_('Quantity'))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    item_options = forms.ModelChoiceField(queryset=ItemOptions.objects.all())
    override_item_options = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    extra_item_options = forms.ModelChoiceField(queryset=ExtraItemOptions.objects.all())
    override_extra_item_options = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    