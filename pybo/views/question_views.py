#질문관리
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

@login_required(login_url='common:login')
# 로그인을 하지 않은 채 질문/답변을 작성할 경우 자동으로 로그인 화면이 뜨도록 해줌
def question_create(request):
    """
    pybo 질문등록
    """
    # GET, POST 방식
    # '질문등록하기'버튼을 누르면 /pybo/question/create/페이지가 GET방식으로 요청되어 question_create 함수가 실행됨
    if request.method=='POST':
        #질문등록 화면에서 '저장하기'버튼을 누르면 question_create함수가 실행되고
        #request.method값은 POST가 되어 다음 코드들이 실행됨
        form = QuestionForm(request.POST) #request.POST에는 사용자가 입력한 내용들이 담김
        if form.is_valid(): #form이 유효한지 검사
        #form이 유효하면 질문데이터가 생성됨, 
            question=form.save(commit=False)
            question.author=request.user #authro 속성에 로그인 계정 저장
            #form으로 Question 데이터를 저장하기 위한 코드
            #QuestionForm이 Question 모델과 연결된 모델 폼이기 때문에 이와 같이 사용 가능
            #commit=False는 임시저장, 아직 데이터 베이스에는 저장되지 않은 상태
            #그냥 form.save()를 수행하면 Question모델의 create_date에 값이 없다는 오류가 뜸
            question.create_date=timezone.now()
            question.save()
            #실제 저장
            return redirect('pybo:index')
    else:#form에 저장된 subject, content값이 올바르지 않으면 오류 메시지가 저장되고, 질문 등록 화면에 표시됨
        form=QuestionForm()
    context={'form':form}
    return render(request, 'pybo/question_form.html', context)
        #render 함수에 전달한 {'form':form}은 템플릿에서 질문 등록시 사용할 폼 엘리먼트를 생성할 때 쓰임


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question=get_object_or_404(Question, pk=question_id)
    # 로그인한 사용자와 글쓴이가 다르면 수정권한이 없다는 오류를 발생시킴-> messages 모듈 이용
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    # POST 요청인 경우
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question=form.save(commit=False)
            question.modify_date = timezone.now() #수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    # GET 요청인 경우
    else:
        form = QuestionForm(instance=question)
    context={'form':form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question=get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

