from django.forms import ModelForm
from .models import Task
from django import forms


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title","description", "important"]
        labels = {
            'title':'',
            'description':''
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':"New Title"}),
            'description': forms.Textarea(attrs={'class':'form-control mb-3', 'placeholder':"New Description"}),
            'important': forms.CheckboxInput(attrs={'class':'form-control form-check-input m-auto', 'placeholder':"New Description"})
        }