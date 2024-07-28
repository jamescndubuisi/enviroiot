from django.contrib import admin

# Register your models here.
from django.contrib import admin
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin


class CustomTokenAdmin(TokenAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)


# Unregister the default TokenAdmin
# admin.site.unregister(Token)

# Register our CustomTokenAdmin
admin.site.register(Token, CustomTokenAdmin)