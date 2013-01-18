from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from models import *


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('user',)
        
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(CompanyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(CompanyForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('user',)
        
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(PersonForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(PersonForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(PositionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(PositionForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(InterviewForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(InterviewForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(ApplyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(ApplyForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class LunchForm (forms.ModelForm):
    time = forms.TimeField(help_text='ex: 10:30am', input_formats=['%H:%M', '%I:%M%p', '%I:%M %p'])
    class Meta:
        model = Lunch
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(LunchForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(LunchForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class NetworkingForm(forms.ModelForm):
    class Meta:
        model = Networking
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(NetworkingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(NetworkingForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class GratitudeForm(forms.ModelForm):
    class Meta:
        model = Gratitude
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(GratitudeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(GratitudeForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(ConversationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(ConversationForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class PitchForm(forms.ModelForm):
    class Meta:
        model = Pitch
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(PitchForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(PitchForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class OnlinePresenceForm(forms.ModelForm):
    class Meta:
        model = OnlinePresence
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(OnlinePresenceForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(OnlinePresenceForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

class PARForm(forms.ModelForm):
    """
    Form to enter and edit stories in PAR(Problem, action, result) format. 
    """
    class Meta:
        model = PAR
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(PARForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(PARForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst

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
        return self.cleaned_data       

class LoginForm(forms.Form):
    username = forms.CharField(label=_('User Name'))
    password = forms.CharField(label=_('Password'), 
            widget =forms.PasswordInput(render_value=False))
