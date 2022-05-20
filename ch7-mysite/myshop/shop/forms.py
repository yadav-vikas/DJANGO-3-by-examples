from pyexpat import model
from django import forms
from .models import ItemOptions, ExtraItemOptions

class ItemOptionsForm(forms.ModelForm):
    class Meta:
        model = ItemOptions
        fields = ['Product_name_item_options', 'option_name_item_options','price_item_options']

class ExtraItemOptionsForm(forms.ModelForm):
    class Meta:
        model = ExtraItemOptions
        fields = ['Product_name_extra_item_options', 'option_name_extra_item_options','price_extra_item_options']
