from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from people.forms import LoginForm
from people.models import BluetoothTag


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'people/login.html'

    def get_success_url(self):
        return reverse('pandemic:editor_main')

    def form_valid(self, form):
        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            if user.team:
                user.team.logged_in = user
                user.team.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)


class LogoutView(View):
    def post(self, request):
        if request.user and request.user.team:
            request.user.team.logged_in = None
            request.user.team.save()
        logout(request)
        return HttpResponseRedirect(reverse('people:login'))


class BluetoothTagList(View):
    def get(self, request):
        addresses = list(BluetoothTag.objects.values_list('address', flat=True))
        return JsonResponse(addresses, safe=False)
