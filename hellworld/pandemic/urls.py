from django.urls import path

from .views import EditorView

urlpatterns = [
    path('submit/', EditorView.as_view(), name='editor_submit')
]