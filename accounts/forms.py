from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from .utils import is_image_file


class SignupForm(UserCreationForm):
    """ This forms helps a user to create an account. """

    SELECT_GENDER = (
        (None, '-- Select your gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    username = forms.CharField(widget=forms.TextInput(attrs={
           'type': 'text', 'class': 'mb-2', 'autofocus': True,
        }),
        required=True,
    )
    mobile_no = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'tel', 'class': 'mb-0',
        }),
        help_text='Enter your phone number and include your country code, e.g. +254112345678'
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'type': 'email', 'class': 'mb-2',
        }),
    )
    gender = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_GENDER,
    )
    dob = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'mb-2',
        }),
        required=True,
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_no', 'gender', 'dob', 'password1', 'password2']


class EditProfileForm(forms.ModelForm):
    """ This form allows a user to edit his/her profile. """

    SELECT_GENDER = (
        (None, '-- Select your gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text', 'class': 'mb-2', 'autofocus': True
        }),
        required=True,
        disabled=True,
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={
           'type': 'text', 'class': 'mb-2',
        }),
        required=True,
        disabled=True,
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'type': 'email', 'class': 'mb-2',
        }),
        disabled=True,
    )
    gender = forms.ChoiceField(widget=forms.Select(attrs={
            'type': 'select', 'class': 'mb-2',
        }),
        choices=SELECT_GENDER,
        disabled=True,
    )
    dob = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date', 'class': 'mb-2',
        }),
        required=True,
        disabled=True,
    )
    mobile_no = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'tel', 'class': 'mb-0',
        }),
        help_text='Enter your phone number and include your country code, e.g. +254112345678'
    )
    profile_pic = forms.FileField(
        widget=forms.FileInput(attrs={
            'type': 'file', 'class': 'form-control mb-2', 'accept': '.jpg, .jpeg, .png',
        }),
        required=False,
        validators=[is_image_file],
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'dob', 'mobile_no', 'profile_pic']
