from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from userauths.models import User
from userauths.models import UserQuizFormula
from django.core.exceptions import ValidationError

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserQuizFormulaForm(forms.ModelForm):
    class Meta:
        model = UserQuizFormula
        fields = ['question_left', 'e_factor', 'interval', 'half_life', 'time_interval']


class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("The two password fields didn't match.")
        return password2

class QuizForm(forms.Form):
    answer = forms.CharField(max_length=255)