from django import forms
 

from .models import Request,Token
from django.contrib.auth import get_user_model
import random
import datetime

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





'''
class TokenForm(forms.ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Token
        fields = ['signature', 'receiver', 'token', 'expiry_date']  
        widgets = {
            'signature': forms.TextInput(attrs={'placeholder': 'Signature','class': 'w-full py-4 px-6 rounded-xl'}),
            'receiver': forms.TextInput(attrs={'placeholder': 'Receiver','class': 'w-full py-4 px-6 rounded-xl'}),
            'token': forms.TextInput(attrs={'placeholder': 'Token','class': 'w-full py-4 px-6 rounded-xl'}),
        }      '''



class TokenForm(forms.ModelForm):
    expiry_choices = [('1 Week', '1 Week'), ('1 Month', '1 Month'), ('3 Months', '3 Months')]
    expiry_date_choice = forms.ChoiceField(choices=expiry_choices)

    class Meta:
        model = Token
        fields = ['signature', 'receiver']

    def clean_expiry_date_choice(self):
        expiry_date_choice = self.cleaned_data['expiry_date_choice']
        if expiry_date_choice == '1 Week':
            expiry_date = datetime.date.today() + datetime.timedelta(weeks=1)
        elif expiry_date_choice == '1 Month':
            expiry_date = datetime.date.today() + datetime.timedelta(days=30)
        elif expiry_date_choice == '3 Months':
            expiry_date = datetime.date.today() + datetime.timedelta(days=90)
        return expiry_date

    def save(self, commit=True):
        token = str(random.randint(0, 9999))
        expiry_date = self.clean_expiry_date_choice()
        instance = super().save(commit=False)
        instance.token = token
        instance.expiry_date = expiry_date
        if commit:
            instance.save()
        return instance