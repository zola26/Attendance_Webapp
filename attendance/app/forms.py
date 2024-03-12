from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'major', 'year', 'starting_year', 'image', 'email', 'password']
       
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'major': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter major'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter year'}),
            'starting_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter starting year'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'password'}),
        }