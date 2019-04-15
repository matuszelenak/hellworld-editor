from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from pandemic.views import EditorView, BluetoothTagSubmitView, ActiveDiseaseInstancesView, \
    CompetitionRules, ADHDPagesView, MedicineInventory, PurchaseMedicine, YawnView, FluView, SneezeView, ResourceView, DiseaseBalance
app_name = 'pandemic'

urlpatterns = [
    url(r'^main/$', login_required(EditorView.as_view()), name='editor_main'),
    url(r'^bluetooth_tag/$', csrf_exempt(BluetoothTagSubmitView.as_view()), name='tag_submit'),
    url(r'^active_diseases/$', csrf_exempt(ActiveDiseaseInstancesView.as_view()), name='active_diseases'),
    url(r'^rules/$', CompetitionRules.as_view(), name='rules'),
    url(r'^adhd/$', ADHDPagesView.as_view(), name='adhd'),
    url(r'^flu/$', FluView.as_view(), name='flu'),
    url(r'^yawn/$', YawnView.as_view(), name='yawn'),
    url(r'^sneeze/$', SneezeView.as_view(), name='sneeze'),
    url(r'^medicine/$', MedicineInventory.as_view(), name='thefuck'),
    url(r'^buy_medicine/$', PurchaseMedicine.as_view(), name='buy_medicine'),

    url(r'^resources/$', ResourceView.as_view(), name='resources'),
    url(r'^resources/(?P<team_pk>\d+)/$', csrf_exempt(ResourceView.as_view()), name='add_resources'),

    url(r'^balance/$', DiseaseBalance.as_view(), name='balance'),
    url(r'^balance/(?P<disease_pk>\d+)/$', csrf_exempt(DiseaseBalance.as_view()), name='set_balance')
]
