from django import forms
from django.contrib.auth.models import User
from .models import *

class ItemForm(forms.ModelForm):
    name = 'ItemForm'
    class Meta:
        model = Item
        fields = ['name', 'thumbnail','description','price']



class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user','is_team']
        

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['user','profile']

class RatingForm(forms.ModelForm):
    
    class Meta:
        model = Rating
        fields = '__all__'
        exclude = ['user','profile']

