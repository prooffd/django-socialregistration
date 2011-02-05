from django import forms
from django.utils.translation import gettext as _

from django.contrib.auth.models import User
from prooffd.accounts.models import UserProfile
from prooffd.documents.models import GRADES

class UserForm(forms.Form):

    username = forms.RegexField(r'^\w+$', max_length=32)
    email = forms.EmailField(required=False)
    grade = forms.ChoiceField(choices=GRADES, help_text="This will help us appropriately match your documents")

    def __init__(self, user, profile, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = user
        self.profile = profile

        if self.user.email:
            del self.fields['email']


    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        else:
            raise forms.ValidationError(_('This username is already in use.'))

    def save(self, request=None):
        self.user.username = self.cleaned_data.get('username')
        if not self.user.email:
            self.user.email = self.cleaned_data.get('email')
        self.user.save()
        user_profile = UserProfile()
        user_profile.user = self.user
        user_profile.grade = self.cleaned_data.get('grade')
        user_profile.save()
        self.profile.user = self.user
        self.profile.save()
        return self.user
