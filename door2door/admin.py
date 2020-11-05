from django.contrib import admin

from door2door.models import StreetTypeModel


@admin.register(StreetTypeModel)
class StreetTypeModelAdmin(admin.ModelAdmin):
    fields = ('pk', 'name', 'short_name')
    list_display  = ('pk', 'name', 'short_name')
    readonly_fields = ('pk',)
    list_display_links = ('name',)
