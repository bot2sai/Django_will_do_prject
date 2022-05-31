from venv import create
from django.contrib import admin
from .models import WillDo

class WillDoAdmin(admin.ModelAdmin):
    readonly_fields = ('creacted',)

admin.site.register(WillDo, WillDoAdmin)
