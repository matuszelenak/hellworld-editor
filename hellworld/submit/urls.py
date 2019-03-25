from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import CodeSubmitAPIView, TaskAssignmentAPIView, SubmitStatusRequestView

app_name = 'submit'

urlpatterns = [
    url(r'^submit/$', csrf_exempt(CodeSubmitAPIView.as_view()), name='code_submit'),
    url(r'^submit/(?P<submit_pk>\d+)/$', SubmitStatusRequestView.as_view(), name='submit_status'),
    url(r'^assignment/(?P<task_pk>\d+)/$', TaskAssignmentAPIView.as_view(), name='task_assignment')
]