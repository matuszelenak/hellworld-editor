from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, TemplateView

from people.forms import LoginForm
from people.models import BluetoothTag, Team
from submit.models import Task, SubmitScore, Submit


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'people/login.html'

    def get_success_url(self):
        return reverse('pandemic:editor')

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
        print(request.body)
        print(request.POST)
        if request.user and request.user.team:
            request.user.team.logged_in = None
            request.user.team.save()
        logout(request)
        return HttpResponseRedirect(reverse('people:login'))


class BluetoothTagList(View):
    def get(self, request):
        addresses = list(BluetoothTag.objects.values_list('address', flat=True))
        return JsonResponse(addresses, safe=False)


class ScoreboardView(TemplateView):
    template_name = 'people/scoreboard.html'

    def get_context_data(self, **kwargs):
        teams = Team.objects.all()
        data = super().get_context_data(**kwargs)
        data['team_scores'] = {}
        for team in teams:
            team_points = 0
            for task in Task.objects.all():
                best_task_score = SubmitScore.objects.filter(
                    submit__participant__team=team,
                    submit__task=task).order_by('-points').first()
                if best_task_score:
                    team_points += best_task_score.points

            solved = set([
                submit.task.name for submit in Submit.objects.filter(participant__team=team, status=Submit.STATUS_OK)
            ])
            data['team_scores'][team.name] = {
                'points': team_points,
                'solved': solved,
                'money': team.resources
             }
        return data
