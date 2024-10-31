from django.contrib import admin
from mymainapp.models import Brand, BrandProfile


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Brand, BrandAdmin)
admin.site.register(BrandProfile)