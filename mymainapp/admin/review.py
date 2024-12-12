from django.contrib import admin
from mymainapp.models import Review
from django.utils import timezone



class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('rating', 'isVisible')
    def save_model(self, request, obj, form, change):
        obj.date_modified = timezone.now()
        super().save_model(request, obj, form, change)


admin.site.register(Review, ReviewAdmin)