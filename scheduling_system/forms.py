from django import forms
from .models import Therapist


class TherapistRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    specialization = forms.CharField(max_length=100)
    experience_years = forms.IntegerField(min_value=0)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


class ParentRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    child_name = forms.CharField(max_length=100, label="Child's Name")
    child_age = forms.IntegerField(label="Child's Age", min_value=0)
    child_diagnosis = forms.CharField(
        max_length=200, label="Child's Diagnosis")


class TherapistEditForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = ['phone_number', 'specialization',
                  'experience_years', 'availability']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Phone Number'}),
            'specialization': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Specialization'}),
            'experience_years': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Experience (Years)'}),
            'availability': forms.Select(attrs={'class': 'input'}),
        }
