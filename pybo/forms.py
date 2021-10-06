# 폼(form):페이지 요청시 전달되는 파라미터들을 쉽게 관리하기 위해 사용하는 클래스
# 필수 파라미터의 값이 누락되지 않았는지, 파라미터의 형식은 적절한지 등을 검증

from django import forms
from pybo.models import Comment, Question, Answer

#질문 등록시 사용할 QuestionForm
class QuestionForm(forms.ModelForm): #모델폼(forms.ModelForm)을 상속
    #모델폼과 일반폼이 있는데 모델폼은 모델과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할 수 있음
    #모델폼은 이너 클래스인 Meta클래스가 반드시 필요 -> 사용할 모델과 모델의 속성을 적기 위해
    class Meta:
        model=Question #사용할 모델(Question 모델과 연결됨)
        fields=['subject','content'] #QuestionForm에서 사용할 Question 모델의 속성
        labels={ #한글로 고침
            'subject':'제목',
            'content':'내용'
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields=['content']
        labels={
            'content':'답변내용'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content':'댓글내용',
        }