from django.contrib import admin
from .models import Maker, ScentNote, Candle, Review, List, ListItem

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


class ListItemAdmin(admin.ModelAdmin):
    list_display = ('candle_id', 'list_id')


admin.site.register(ListItem, ListItemAdmin)
