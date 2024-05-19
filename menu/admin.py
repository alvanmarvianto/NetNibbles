from django.contrib import admin
from .models import Menu

class MenuAdmin(admin.ModelAdmin):
  list_display = ("name", "category", "price",)
  
admin.site.register(Menu, MenuAdmin)
