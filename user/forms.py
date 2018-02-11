from django import forms as f
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class CreateUser(f.ModelForm):
	password = f.CharField(widget=f.PasswordInput)
	password2 = f.CharField(label="Confirmer mot de passe",widget=f.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean(self):
		cleaned_data = super().clean()
		email = self.cleaned_data.get('email')
		password = self.cleaned_data('password')
		password2 = self.cleaned_data('password2')
		
		if User.objects.filter(email=email).exists():
			self.add_error("email","Cet email existe déja !")
		if password and password and password!=password2:
			self.add_error("password2","Mots de passe non identiques!")
		return cleaned_data

class AdminCreateUser(f.ModelForm):
	password = f.CharField(widget=f.PasswordInput)
	password2 = f.CharField(label="Confirmer mot de passe",widget=f.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)
	def clean_password2(self):
		password = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if password and password2 and password != password2:
			raise f.ValidationError("Mots de passe non identiques!")
		return password2

	def save(self,commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user
class AdminChangeUser(f.ModelForm):
	password = ReadOnlyPasswordHashField()
	class Meta:
		model = User
		fields = ('email','password','active','admin','staff')
	def clean_password(self):
		return self.initial["password"]