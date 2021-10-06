# 기본 관리(index, detail)
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page=request.GET.get('page','1') #페이지
    # get방식으로 호출된 url(ex.http://localhost:8000/pybo/?page=1)에서 page값을 가져올 때 사용
    kw=request.GET.get('kw', '') #화면으로 부터 전달받은 검색어
    so=request.GET.get('so', 'recent') #정렬 기준, 최초 : 최신순

    #정렬
    if so == 'recommend': #추천 수가 많은순
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular': #답글 수가 많은순
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:      # recent : #최신순
        question_list = Question.objects.order_by('-create_date')
    
    #검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색(kw가 포함되어 있는지)
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains = kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    #페이징처리
    paginator=Paginator(question_list, 10) #페이지당 10개씩 보여주기
    # question_list:게시물 전체, 10:페이지당 보여줄 개수
    page_obj=paginator.get_page(page)
    # 요청된 페이지에 해당되는 페이징 객체 생성-> 장고는 내부적으로는 데이터 전체를 조회하지 않고 해당 페이지 데이터만 조회
    context={'question_list': page_obj,'page':page, 'kw':kw, 'so':so}
    
    return render(request, 'pybo/question_list.html', context)
    #render() 파이썬 데이터를 템플릿에 적용하여 html로 반환함


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id) #pk:primary key(기본 키)
    context = {'question': question }
    return render(request, 'pybo/question_detail.html', context)
