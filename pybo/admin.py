from django.contrib import admin
from.models import Question


class QuestionAdmin(admin.ModelAdmin): #세부기능 구현
    search_fields=['subject'] #제목 검색


admin.site.register(Question, QuestionAdmin)
# Register your models here.
