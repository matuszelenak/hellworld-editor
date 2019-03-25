from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from pandemic.views import EditorView

app_name = 'pandemic'

urlpatterns = [
    url(r'^main/$', login_required(EditorView.as_view()), name='editor_main'),
]