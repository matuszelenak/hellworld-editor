from django.urls import path

from .views import CodeSubmitAPIView

urlpatterns = [
    path('submit/', CodeSubmitAPIView.as_view(), name='code_submit')
]