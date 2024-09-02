from django.contrib import admin
from .models import Brand, ScentNote, Candle, Review, List, ListItem, Report, ScentGenre, ScentFamily


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Brand, BrandAdmin)

admin.site.register(ScentFamily)
admin.site.register(ScentGenre)
admin.site.register(ScentNote)



class CandleAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand_id', 'date_modified')
    readonly_fields = ('gid',)


admin.site.register(Candle, CandleAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('rating', 'isVisible')


admin.site.register(Review, ReviewAdmin)

class ListAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'list_type', 'isActive',)
    readonly_fields = ('gid',)
admin.site.register(List, ListAdmin)


class ListItemAdmin(admin.ModelAdmin):
    list_display = ('candle_id', 'list_id')



admin.site.register(ListItem, ListItemAdmin)

class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('reporter', 'report_type', 'review_id', 'report_text', 'date_created', )


admin.site.register(Report, ReportAdmin)

