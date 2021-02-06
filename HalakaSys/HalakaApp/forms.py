from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Students ,Degree,Contact
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.utils.timezone import now
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget

class UserForm(UserCreationForm):
       class Meta():
        model = User
        fields = ('username',  'password1', 'password2')
        labels = {
        'password1':'Password',
        'password2':'Confirm Password'
        }
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Students
        fields = ('ikama_number' , 'firstname', 'other_name', 'surname', 'center_id', 'sex', 'course_id')




class ExcludedDegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = "__all__"

    def __init__(self, user, *args, **kwargs):
        super(ExcludedDegreeForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['stud_id']=forms.ModelChoiceField(queryset =
            Students.objects.filter(staff_id__author = user), label="اسم الطالب ")
            self.fields['stud_id'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data


class DegreeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DegreeForm, self).__init__(*args, **kwargs)
        self.fields['stud_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Degree
        fields = "__all__"

class DegreeForm2(forms.ModelForm):

    class Meta:
        model = Degree
        fields = "__all__"




