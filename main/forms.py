from django.forms import ModelForm
from main.models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['category']


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        # exclude = ['product_count']


class OutputForm(ModelForm):
    class Meta:
        model = Output
        fields = "__all__"


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ['total1', 'total2', 'total3', 'total4', 'total_amount']
