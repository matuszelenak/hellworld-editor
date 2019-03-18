from django import forms
from django.core.files.base import ContentFile

from submit.models import Submit


class CodeSubmitForm(forms.ModelForm):
    code = forms.Textarea()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        self.user = request.user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.file = ContentFile(self.cleaned_data['code'])
        super().__init__(commit)

    class Meta:
        model = Submit
        fields = ('language', )
