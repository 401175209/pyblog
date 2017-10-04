from django import forms
from .models import comment

class commentform(forms.ModelForm):
    class Meta:
        model=comment
        fields=['name','email','text']