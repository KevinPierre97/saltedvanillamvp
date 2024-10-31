from django.contrib import admin
from mymainapp.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('rating', 'isVisible')


admin.site.register(Review, ReviewAdmin)