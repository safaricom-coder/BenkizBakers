from django import forms
from django.contrib.auth.models import User
from .models import Item,UserProfile

class ItemForm(forms.ModelForm):
    name = 'ItemForm'
    class Meta:
        model = Item
        fields = ['name', 'thumbnail','description','price']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number','profilepic','lastname','country','county','address_or_street','apartment_or_house_name_or_number']
        

        
        
# class CustomUserCreationForm(forms.ModelForm):
    
#     email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Type Mail ...:','label':"email"}),max_length=20,required=True)
#     username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Type Name ...:','label':"name"}),max_length=20,required=True)
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Desired password ...:','label':"name"}),max_length=20,required=True)
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password ...:','label':"name"}),max_length=20,required=True)
#     class Meta:
#         model = User
#         fields = ['username','password1','password2','email']
        
#         def save(self,commit=True):
#             user = super().save(commit=False)
#             user.email = self.cleaned_data['email']
#             if commit:
#                 user.save()
#             return user
            