from django.contrib import admin
from mymainapp.models import Report


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('reporter', 'report_type', 'review_id', 'report_text', 'date_created', )


admin.site.register(Report, ReportAdmin)