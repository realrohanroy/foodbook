from django import forms
from .models import CustomUser , Recipe, Review
from django.contrib.auth.forms import UserCreationForm
from image_cropping import ImageCropWidget
from django.contrib.auth import get_user_model

from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image', 'cooking_time']  # Include other fields as necessary

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser .objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser  
        fields = ['first_name', 'last_name', 'profile_picture', 'profile_picture_cropping']
        widgets = {
            'profile_picture_cropping': ImageCropWidget,
        }