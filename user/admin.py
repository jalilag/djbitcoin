from django.contrib import admin
from django.contrib.auth.models import Group
from  django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

from .forms import AdminCreateUser,AdminChangeUser
from .models import User

class UserAdmin(BaseUserAdmin):
	form = AdminChangeUser
	add_form = AdminCreateUser

	list_display = ('email','password')
	list_filter = ('email',)
	fieldsets = (
		# (None,{'fields':('email','password')}),
		('Info personelles',{'fields':('email','password'),}),
		('Permissions',{"fields":('admin',)})		
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password', 'password2')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(User,UserAdmin)
admin.site.unregister(Group)