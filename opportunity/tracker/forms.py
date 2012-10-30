from django import forms

from models import Apply
from models import Company
from models import Person
from models import Position
from models import Interview
from models import Networking
from models import Gratitude
from models import Conversation

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


