from django import forms
from .models import Bird, JudgeEvaluation, VisitorVote
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BirdUploadForm(forms.ModelForm):
    class Meta:
        model = Bird
        fields = ['name', 'category', 'description', 'image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class JudgeEvaluationForm(forms.ModelForm):
    class Meta:
        model = JudgeEvaluation
        fields = ['score', 'comments']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['score'].widget.attrs.update({'class': 'form-control'})
        self.fields['comments'].widget.attrs.update({'class': 'form-control', 'rows': 3})

class VisitorVoteForm(forms.Form):
    bird_id = forms.IntegerField(widget=forms.HiddenInput())

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
