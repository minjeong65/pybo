from django.contrib.auth.models import User
from django.db import models
#모델 변경 후 cmd창에서 makemigrations 와 migrate를 통해 데이터베이스 변경해야함

class Question(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='author_question',null=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question') #추천인 추가

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='author_answer',null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    # 수정일시는 수정할 때에만 표시되므로 null=True, blank=True를 사용하여 값을 비워둘 수 있게 함
    voter=models.ManyToManyField(User, related_name='voter_answer')
    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) #댓글 글쓴이
    content = models.TextField()    #댓글 내용
    create_date=models.DateTimeField()  #댓글 작성일시
    modify_Date=models.DateTimeField(null=True, blank=True) #댓글 수정일시
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE) #이 댓글이 달린 질문
    answer=models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)   #이 댓글이 달린 답변
    #CASCADE : 질문이나 답변이 삭제될 경우 같이 삭제되도록
