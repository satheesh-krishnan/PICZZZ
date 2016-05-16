from django import forms
from django.contrib.auth.models import User
from pic.models import UserProfile,Photos

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','first_name','last_name','password','email')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('profile_picture',)

class PictureForm(forms.ModelForm):
	class Meta:
		model = Photos
		fields = ('upload_photo',)


class SearchForm(forms.Form):
    search = forms.CharField(required=False,initial='',widget=forms.TextInput(attrs={'size':40}))
