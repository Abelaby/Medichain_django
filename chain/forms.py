from django import forms
 

from .models import Request,Token
from django.contrib.auth import get_user_model

User = get_user_model()
data_subjects = User.objects.filter(Data_Subject=True)



class RequestForm(forms.ModelForm):
    Ds_name = forms.ChoiceField(
        choices=[(user.username, user.username) for user in data_subjects], 
        widget=forms.Select(attrs={'class': 'w-full bg-gray-100 p-3 rounded-lg'}),
    )    
    class Meta:
        model = Request
        fields = ['Rqp_name', 'Ds_name']
        widgets = {
            'Rqp_name': forms.TextInput(attrs={'placeholder': 'Requesting Party', 'class': 'w-full bg-gray-100 p-3 rounded-lg mb-4'}),
        }






class TokenForm(forms.ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Token
        fields = ['signature', 'receiver', 'token', 'expiry_date']  
        widgets = {
            'signature': forms.TextInput(attrs={'placeholder': 'Signature','class': 'w-full py-4 px-6 rounded-xl'}),
            'receiver': forms.TextInput(attrs={'placeholder': 'Receiver','class': 'w-full py-4 px-6 rounded-xl'}),
            'token': forms.TextInput(attrs={'placeholder': 'Token','class': 'w-full py-4 px-6 rounded-xl'}),
        }      