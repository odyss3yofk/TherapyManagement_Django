from django import forms
from .models import Therapist, Parent, Child, TherapySession


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
        fields = [
            'phone_number',
            'specialization',
            'experience_years',
            'available_morning',
            'available_afternoon',
            'available_evening'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Phone Number'}),
            'specialization': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Specialization'}),
            'experience_years': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Experience (Years)'}),
            'available_morning': forms.CheckboxInput(attrs={'class': 'input'}),
            'available_afternoon': forms.CheckboxInput(attrs={'class': 'input'}),
            'available_evening': forms.CheckboxInput(attrs={'class': 'input'}),
        }


class ParentDashboardForm(forms.ModelForm):

    child_name = forms.CharField(
        max_length=100,
        label="Child's Name",
        widget=forms.TextInput(
            attrs={'class': 'input', 'placeholder': "Child's Name"})
    )
    child_age = forms.IntegerField(
        label="Child's Age",
        min_value=0,
        widget=forms.NumberInput(
            attrs={'class': 'input', 'placeholder': "Child's Age"})
    )
    child_diagnosis = forms.CharField(
        max_length=200,
        label="Child's Diagnosis",
        widget=forms.TextInput(
            attrs={'class': 'input', 'placeholder': "Diagnosis"})
    )

    class Meta:
        model = Parent
        fields = ['name', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': "Parent's Name"}),
            'phone_number': forms.TextInput(attrs={'class': 'input', 'placeholder': "Phone Number"}),
        }


class SessionForm(forms.ModelForm):
    class Meta:
        model = TherapySession
        fields = [
            'therapist',
            'child',
            'date',
            'time',
            'duration_minutes',
            'notes',
        ]
        widgets = {
            'therapist': forms.Select(attrs={'class': 'input'}),
            'child': forms.Select(attrs={'class': 'input'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'input'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Duration (minutes)'}),
            'notes': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Notes', 'rows': 2}),
        }
