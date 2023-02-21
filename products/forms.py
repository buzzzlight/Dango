from django import forms
from .models import Products


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            "title",
            "content",
            "price",
            "image",
        ]
        labels = {
            "title": "상품 이름",
            "content": "상품 정보",
            "price": "가격",
        }