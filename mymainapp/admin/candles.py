from django.contrib import admin
from mymainapp.models import Candle


class CandleAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand_id', 'date_modified')
    readonly_fields = ('gid',)


admin.site.register(Candle, CandleAdmin)