from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from models import Apply
from models import Company
from models import Person
from models import Position
from models import Interview
from models import Networking
from models import Gratitude
from models import Conversation
from models import UserProfile

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview

class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply

class NetworkingForm(forms.ModelForm):
    class Meta:
        model = Networking

class GratitudeForm(forms.ModelForm):
    class Meta:
        model = Gratitude

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label=_('User Name'))
    email = forms.EmailField(label=_('Email Address'))
    password = forms.CharField(label=_('Password'), 
				widget =forms.PasswordInput(render_value=False))
    password_verify = forms.CharField(label=_('Verify password'), 
				widget =forms.PasswordInput(render_value=False))
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def clean_username(self):
        ''' 
        Methods prefixed with 'clean_' and concatenated 
        with a variable name are used to valid that variable.
        This method makes sure there isn't a user by this 
        name already in the database. 
        '''
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_('That user name is taken. Please, select another'))


    def clean(self):
        ''' 
        To validate the password, we need two fields. clean is called
        with all. 
        '''
        password = self.cleaned_data['password']
        password_verify = self.cleaned_data['password_verify']
        if password != password_verify:
            raise forms.ValidationError(_('The passwords did not match'))
        # import pdb; pdb.set_trace()
        return self.cleaned_data       

class LoginForm(forms.Form):
    username = forms.CharField(label=_('User Name'))
    password = forms.CharField(label=_('Password'), 
            widget =forms.PasswordInput(render_value=False))
