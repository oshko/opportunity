from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .models import *


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'division', 'address', 'city',
                  'state_province', 'country', 'zipCode',
                  'website')

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
        fields = ('first_name', 'last_name', 'title', 'company')

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
        fields = ('company', 'title', 'website')

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
    time = forms.TimeField(
        help_text='ex: 10:30am',
        input_formats=['%H:%M', '%I:%M%p', '%I:%M %p'])

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
    time = forms.TimeField(
        help_text='ex: 10:30am',
        input_formats=['%H:%M', '%I:%M%p', '%I:%M %p'])

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
    time = forms.TimeField(
        help_text='ex: 10:30am',
        input_formats=['%H:%M', '%I:%M%p', '%I:%M %p'])

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
    time = forms.TimeField(
        help_text='ex: 10:30am',
        input_formats=['%H:%M', '%I:%M%p', '%I:%M %p'])

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


class MeetingMentorForm(forms.ModelForm):
    time = forms.TimeField(
        help_text='ex: 10:30am',
        input_formats=['%H:%M', '%I:%M%p', '%I:%M %p'])

    class Meta:
        model = MentorMeeting
        exclude = ('user', 'mentorship',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(MeetingMentorForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(MeetingMentorForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst


class MentorshipForm(forms.ModelForm):
    jobseeker = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(role=UserProfile.JOB_SEEKER))
    mentor = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(role=UserProfile.MENTOR))

    class Meta:
        model = Mentorship
        fields = (
            'jobseeker',
            'mentor',
            'startDate',
            )


class ConversationForm(forms.ModelForm):
    time = forms.TimeField(
        help_text='ex: 10:30am',
        input_formats=['%H:%M', '%I:%M%p', '%I:%M %p'])

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


class PositionCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 80 } ))
    class Meta:
        model = PositionComment
        fields = ('comment',)
        
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(PositionCommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(PositionCommentForm, self).save(commit=False)
        inst.user = self._user
        if commit:
            inst.save()
        return inst


class CompanyCommentForm(PositionCommentForm):
    class Meta:
        model = CompanyComment
        fields = ('comment',)


class InterviewCommentForm(PositionCommentForm):
    class Meta:
        model = InterviewComment
        fields = ('comment',)


class ApplyCommentForm(PositionCommentForm):
    class Meta:
        model = ApplyComment
        fields = ('comment',)


class NetworkingCommentForm(PositionCommentForm):
    class Meta:
        model = NetworkingComment
        fields = ('comment',)


class LunchCommentForm(PositionCommentForm):
    class Meta:
        model = LunchComment
        fields = ('comment',)


class MentorMeetingCommentForm(PositionCommentForm):
    class Meta:
        model = MentorMeetingComment
        fields = ('comment',)


class ConversationCommentForm(PositionCommentForm):
    class Meta:
        model = ConversationComment
        fields = ('comment',)


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label=_('User Name'))
    first_name = forms.CharField(label=_('First name'), max_length=30)
    last_name = forms.CharField(label=_('Last name'), max_length=30)
    email = forms.EmailField(label=_('Email Address'))
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(render_value=False))
    password_verify = forms.CharField(
        label=_('Verify password'),
        widget=forms.PasswordInput(render_value=False))
    # Users can select either job seeker or mentor.
    # coordinator is not granted via the UI.
    role = forms.ChoiceField(
        label="Label",
        choices=[r for r in UserProfile.ROLES_AT_UPGLO
                 if UserProfile.COORDINATOR not in r]
    )

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'first_name',
            'last_name',
            'title',
            'role',
            'email',
            'password',
            'password_verify'
        )

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
        raise forms.ValidationError(
            "That user name is taken."
            " Please, select another")

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
                               widget=forms.PasswordInput(render_value=False))
