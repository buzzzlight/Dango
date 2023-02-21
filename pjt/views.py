from django.shortcuts import render
from products.models import Products

def main(request):
    products = Products.objects.order_by('-pk')
    context = {
        "products": products,
    }
    return render(request, "main.html", context)