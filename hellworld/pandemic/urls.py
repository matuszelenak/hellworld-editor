from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from pandemic.views.administration import ResourceView, DiseaseBalance
from pandemic.views.diseases import ActiveDiseaseInstancesView, ADHDImagesPaths
from pandemic.views.editor import EditorView, BluetoothTagSubmitView,  MedicineInventory, PurchaseMedicine

app_name = 'pandemic'

urlpatterns = [
    # Editor
    url(r'^$', login_required(EditorView.as_view()), name='editor'),
    url(r'^bluetooth_tag/$', csrf_exempt(BluetoothTagSubmitView.as_view()), name='tag_submit'),
    url(r'^medicine/$', MedicineInventory.as_view(), name='medicine_inventory'),
    url(r'^buy_medicine/$', PurchaseMedicine.as_view(), name='medicine_purchase'),

    # Diseases
    url(r'^active_diseases/$', csrf_exempt(ActiveDiseaseInstancesView.as_view()), name='active_diseases'),
    url(r'^adhd_images/$', ADHDImagesPaths.as_view(), name='adhd_images'),

    # Administration
    url(r'^resources/$', ResourceView.as_view(), name='resources'),
    url(r'^resources/(?P<team_pk>\d+)/$', csrf_exempt(ResourceView.as_view()), name='add_resources'),
    url(r'^balance/$', DiseaseBalance.as_view(), name='balance'),
    url(r'^balance/(?P<disease_pk>\d+)/$', csrf_exempt(DiseaseBalance.as_view()), name='set_balance')
]
