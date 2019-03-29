from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from people.views import LoginView, LogoutView, BluetoothTagList

app_name = 'people'

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', csrf_exempt(LogoutView.as_view()), name='logout'),
    url(r'^tags/', BluetoothTagList.as_view(), name='registered_tags')
]
