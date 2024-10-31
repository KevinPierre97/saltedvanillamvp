from django.contrib import admin
from mymainapp.models import List, ListItem


class ListAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'list_type', 'isActive',)
    readonly_fields = ('gid',)


admin.site.register(List, ListAdmin)


class ListItemAdmin(admin.ModelAdmin):
    list_display = ('candle_id', 'list_id')


admin.site.register(ListItem, ListItemAdmin)
