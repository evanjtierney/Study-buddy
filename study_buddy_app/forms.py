from .models import Profile
from django import forms
from django.contrib.auth.models import User

# class ClassForm(forms.Form):
#     department = forms.CharField(
#         max_length=4,
#         widget=forms.Select(choices=),
#     )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email') # add 'classes'?