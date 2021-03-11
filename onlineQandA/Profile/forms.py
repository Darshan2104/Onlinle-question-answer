from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from crispy_forms.helper import FormHelper
from django.forms import ModelForm, Textarea
from .models import Profile

# Forms


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'gender', 'Address',
                  'education', 'skill', 'about')  # "__all__"
        widgets = {
            'gender': forms.RadioSelect(),
            'Address': Textarea(attrs={'cols': 20, 'rows': 2}),
            'education': Textarea(attrs={'cols': 20, 'rows': 1}),
            # to give css class for specific field
            # 'skill': TaggableManager(attrs={'class':"form-control"}),
            'about': Textarea(attrs={'cols': 20, 'rows': 5}),
        }
    # helper = FormHelper()
    # helper.form_class = 'form-group'
    # helper.layout = Layout(
    #     Field('image', css_class='form-control mt-2 mb-3'),
    #     Field('gender', rows="3", css_class='form-control mb-3'),
    #     Field('Address', css_class='form-control mb-3'),
    #     Field('tags', css_class='form-control mb-3'),
    #     Field('education', css_class='form-control'),
    #     Field('about', css_class='form-control'),
    # )
