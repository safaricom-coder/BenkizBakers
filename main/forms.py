from django import forms
from django.contrib.auth.models import User
from .models import *

class ItemForm(forms.ModelForm):
    name = 'ItemForm'
    class Meta:
        model = Item
        fields = ['name','description','price','numberOfItems','category']



class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user','is_team','is_normal_admin']
        


class RatingForm(forms.ModelForm):
    
    class Meta:
        model = Rating
        fields = '__all__'
        exclude = ['user','profile']

paymentchoices = [
    ('M-Pesa','mpesa'),
    ('Paypal','paypal')
]
class PaymentForm(forms.Form):
    payment = forms.ChoiceField(
        choices=paymentchoices,widget=forms.RadioSelect,label='Payment Option'
    )
