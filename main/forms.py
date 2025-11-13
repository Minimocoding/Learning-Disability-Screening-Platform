from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, ParentProfile, TeacherProfile, PsychologistProfile, Child

class BaseRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ParentRegistrationForm(BaseRegistrationForm):
    PARENT_TYPES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('sibling', 'Sibling'),
        ('other', 'Other'),
    ]
    
    parent_type = forms.ChoiceField(choices=PARENT_TYPES, required=True)

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user_profile = UserProfile.objects.create(user=user, user_type='parent')
            ParentProfile.objects.create(
                user_profile=user_profile,
                parent_type=self.cleaned_data['parent_type']
            )
        return user

class TeacherRegistrationForm(BaseRegistrationForm):
    school_name = forms.CharField(max_length=200, required=True)

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user_profile = UserProfile.objects.create(user=user, user_type='teacher')
            TeacherProfile.objects.create(
                user_profile=user_profile,
                school_name=self.cleaned_data['school_name']
            )
        return user

class PsychologistRegistrationForm(BaseRegistrationForm):
    professional_qualification = forms.CharField(max_length=200, required=True)
    organization_clinic = forms.CharField(max_length=200, required=True)

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            user_profile = UserProfile.objects.create(user=user, user_type='psychologist')
            PsychologistProfile.objects.create(
                user_profile=user_profile,
                professional_qualification=self.cleaned_data['professional_qualification'],
                organization_clinic=self.cleaned_data['organization_clinic']
            )
        return user

class ChildInfoForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'age', 'grade', 'school_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter child\'s name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '3', 'max': '18'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Grade 1, Kindergarten'}),
            'school_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter school name'}),
        }

class TestAnswerForm(forms.Form):
    ANSWER_CHOICES = [
        (0, 'No'),
        (1, 'Sometimes'),
        (2, 'Yes'),
    ]
    
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        
        for question in questions:
            field_name = f'question_{question.question_number}'
            self.fields[field_name] = forms.ChoiceField(
                choices=self.ANSWER_CHOICES,
                widget=forms.RadioSelect(),
                label=question.question_text,
                required=True
            )