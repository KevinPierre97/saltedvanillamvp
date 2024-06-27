from django.contrib import admin
from landingpageapp.models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined')
admin.site.register(Member, MemberAdmin)
