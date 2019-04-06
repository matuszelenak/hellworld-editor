from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from pandemic.views import EditorView, BluetoothTagSubmitView, ActiveDiseaseInstancesView, CompetitionRules, ADHDPagesView

app_name = 'pandemic'

urlpatterns = [
    url(r'^main/$', login_required(EditorView.as_view()), name='editor_main'),
    url(r'^bluetooth_tag/$', csrf_exempt(BluetoothTagSubmitView.as_view()), name='tag_submit'),
    url(r'^active_diseases/$', csrf_exempt(ActiveDiseaseInstancesView.as_view()), name='active_diseases'),
    url(r'^rules/$', CompetitionRules.as_view(), name='rules'),
    url(r'^adhd/$', ADHDPagesView.as_view(), name='adhd')
]
