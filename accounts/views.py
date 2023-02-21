from django.shortcuts import render, redirect
from django.urls import is_valid_path
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def signup(request):
    # 로그인한 회원이 url로 회원가입 하려는 경우 메인페이지로 리턴
    if request.user.is_authenticated:
        return redirect("main")
    # POST 요청 처리
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # ModelForm의 save 메서드의 리턴값은 해당 모델의 인스턴스
            auth_login(request, user) # 회원가입 직후 자동로그인
            return redirect('main')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def mypage(request, pk):
    # user = request.user
    user = get_user_model().objects.get(pk=pk)
    context = {
        "user": user
    }
    return render(request, "accounts/mypage.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("main")
    if request.method == 'POST':
        # AuthenticationForm은 ModelForm이 아님
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 세션 저장
            # login 함수는 request, user 객체를 인자로 받음
            # user 객체는 form에서 인증된 유저 정보로 받을 수 있음
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'main')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('main')


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect("main")