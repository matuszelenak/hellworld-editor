from django.views.generic import FormView

from .forms import CodeSubmitForm


class EditorView(FormView):
    template_name = 'pandemic/editor.html'
    form_class = CodeSubmitForm



