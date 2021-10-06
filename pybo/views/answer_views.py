#답변관리
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

@login_required(login_url='common:login')
def answer_create(request, question_id): #question_id는 URL 매핑에 의해 그 값이 전달됨
    #답변 등록시 텍스트창에 입력한 내용은 request를 통해 읽을 수 있다.
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
    # 답변등록에서는 POST 방식만 사용되므로 else는 호출되지 않지만 패턴의 통일성을 위해 남겨둠
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user #author 속성에 로그인 계정 저장
            answer.create_date=timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id = question.id), answer.id))
    else:
        form=AnswerForm()
    context={'question': question, 'form':form}
    return render(request, 'pybo/question_detail.html',context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변수정
    """
    answer=get_object_or_404(Answer, pk=answer_id)
    if request.user!= answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('{}#answer_{}'.format(
            resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    if request.method == "POST":
        form = AnswerForm(request.POST, instance = answer)

        if form.is_valid():
            answer=form.save(commit=False)
            answer.modify_date=timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance = answer)
    context={'answer':answer,'form':form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변삭제
    """
    answer=get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "삭제권한이 없습니다")
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

