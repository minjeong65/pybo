from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')), #common앱의 urls.py 파일 사용을 위해 수정
    #-> http://localhost:8000/common/ 으로 시작하는 url은 모두 common/urls.py를 참조함
    path('', base_views.index, name='index'), #'/'에 해당되는 path
]
