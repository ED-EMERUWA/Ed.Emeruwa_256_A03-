from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')  # show these columns
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')
