from django import forms
from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=('gender','phone','date_of_birth','post','department','status')