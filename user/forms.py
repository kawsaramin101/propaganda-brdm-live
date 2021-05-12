from django.forms import ModelForm, Textarea, DateInput, DateField
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Profile



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
        widgets = {
            'first_name': Textarea(attrs={'cols': 21,'rows':1 ,'autofocus': True})
        }
        
        
        
class EditProfileForm(ModelForm):
    #birthdate = forms.DateField(widget=forms.DateInput)
    class Meta:
        model = Profile 
        fields = ['profilepic', 'bio', 'birthdate']
        
        widgets = {
            'bio': Textarea(attrs={'cols': 30, 'rows': 4}),
            'birthdate': DateInput(attrs={'placeholder': 'yyyy-mm-dd'})
        }
        #labels = {
            #'profilepic': _('Profile picture'),
        #}
        
        
        
class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
        
        