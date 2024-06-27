from django.contrib import admin
from .models import Maker, ScentNote, Candle, Review, List

admin.site.register(Maker)
admin.site.register(ScentNote)


class CandleAdmin(admin.ModelAdmin):
    list_display = ('name', 'maker_id', 'date_added')
    readonly_fields = ('gid',)


admin.site.register(Candle, CandleAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('rating', 'isVisible')


admin.site.register(Review, ReviewAdmin)

admin.site.register(List)
