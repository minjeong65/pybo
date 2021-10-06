from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from common.forms import UserForm

def signup(request):
    """
    계정생성
    """
    if request.method == "POST": #POST 요청이면 입력한 데이터로 사용자 생성
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user=authenticate(username = username, password= raw_password) #사용자 인증
            #authenticate : 사용자명과 비밀번호가 정확한지 검증하는 함수
            login(request, user) #로그인
            return redirect('index')
    else: #GET 요청이면 계정생성화면을 리턴
        form=UserForm()
    return render(request, 'common/signup.html', {'form':form})
