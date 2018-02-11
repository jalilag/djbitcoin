from django.db import models as m
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email: raise ValueError('Adresse mail manquante !')
		user = self.model(email=self.normalize_email(email))
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staffuser(self, email, password):
		user = self.create_user(email,password=password)
		user.staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None):
		user = self.create_user(email,password=password)
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	email = m.EmailField(verbose_name="Adresse mail",max_length=255,unique=True)
	# password = m.CharField(max_length=32,verbose_name="Mot de passe")
	active = m.BooleanField(default=True)
	staff = m.BooleanField(default=False)
	admin = m.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	def __str__(self):
		return self.email

	def has_perm(self,perm,obj=None):
		return True

	def has_module_perms(self,app_label):
		return True
    
	# property est un décorateur permettant de transformer artificiellement une fonction en méthode
	@property
	def is_staff(self):
	    return self.staff

	@property
	def is_admin(self):
	    return self.admin

	@property
	def is_active(self):
	    return self.active

