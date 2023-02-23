from django.contrib.auth import authenticate, login     # 사용자 인증 / 로그인
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # form.cleaned_data.get : 폼의 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수로 여기서는 인증시 사용할 사용자명과 비밀번호를 얻기 위해 사용
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})