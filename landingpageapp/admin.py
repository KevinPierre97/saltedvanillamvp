from django.contrib import admin
from landingpageapp.models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined')
    readonly_fields = ('referred_by',)

admin.site.register(Member, MemberAdmin)
