from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe
import products
from .forms import ProductsForm
from .models import Products
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    context = {
        'product': product,
    }
    return render(request, "products/detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, '수정 완료')
            return redirect("main")
    else:
        form = ProductsForm()
    context = {
        "form": form,
    }
    return render(request, "products/create.html", context)


@login_required
def update(request, pk):
    product = Products.objects.get(pk=pk)
    if request.user != product.user:
        # (1) 아무말 없이 메인화면으로 보내기
        # return redirect("main")
        # (2) flash message 활용
        # messages.warning(request, '작성자만 수정할 수 있어요!')
        # return redirect('products.detail', product.pk)
        # (3) 403 에러메세지 보내기
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    if request.method == "POST":
        form = ProductsForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:detail", pk)
    else:
        form = ProductsForm(instance=product)
    context = {
        "form": form,
    }
    return render(request, "products/create.html", context)


@login_required
def delete(request, pk):
    product = Products.objects.get(pk=pk)

    if request.user != product.user:
        return redirect("main")

    if request.method == "POST":
        if request.user == product.user:
            product.delete()
            return redirect("main")
    else:
        return redirect("products:detail", pk)


# @login_required
# def like(request, pk):
#     product = Products.objects.get(pk=pk)
#     if product.like_users.filter(id=request.user.id).exists():
#         product.like_users.remove(request.user)
#         is_liked = False
#     else:
#         product.like_users.add(request.user)
#         is_liked = True
#     context = {
#         'isLiked': is_liked,
#         'likeCount': product.like_users.count()
#     }
#     return JsonResponse(context)