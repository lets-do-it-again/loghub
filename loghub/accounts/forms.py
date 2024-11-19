from django import forms
from accounts.admin import User

class UpdateProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name','image_file','professional']


# class ChangePasswordForm(forms.Form):
#     old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
#     new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")