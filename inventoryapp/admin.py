from django.contrib import admin

# Register your models here.
from django.contrib import admin
from inventoryapp.models import Inventory,InventoryUser
# Register your models here.
admin.site.register(Inventory)
admin.site.register(InventoryUser)