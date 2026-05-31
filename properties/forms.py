from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Property, Review
from .models import Profile

class SignupForm(UserCreationForm):

    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('owner', 'Owner'),
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter email'})
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        help_text=''
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        help_text=''
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2'
        ]

class PropertyForm(forms.ModelForm):

    class Meta:

        model = Property

        fields = [
            'title',
            'location',
            'price',
            'property_type',
            'status',
            'image',
            'description',
            'bedrooms',
            'bathrooms',
            'area',
            'map_link'
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'placeholder': 'Enter property title'
            }),

            'location': forms.TextInput(attrs={
                'placeholder': 'Enter location'
            }),

            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter property price'
            }),

            'description': forms.Textarea(attrs={
                'placeholder': 'Write property description',
                'rows': 5
            }),

            'bedrooms': forms.NumberInput(attrs={
                'placeholder': 'Bedrooms'
            }),

            'bathrooms': forms.NumberInput(attrs={
                'placeholder': 'Bathrooms'
            }),

            'area': forms.NumberInput(attrs={
                'placeholder': 'Area in sqft'
            }),

            'map_link': forms.URLInput(attrs={
                'placeholder': 'Google Maps link'
            }),

        }


    
class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review

        fields = ['rating', 'comment']

        widgets = {

            'rating': forms.Select(
                choices=[
                    (1, '1 Star'),
                    (2, '2 Stars'),
                    (3, '3 Stars'),
                    (4, '4 Stars'),
                    (5, '5 Stars'),
                ]
            ),

            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Write your review...'
                }
            )

       }

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'profile_image',
            'phone',
            'bio'
        ]