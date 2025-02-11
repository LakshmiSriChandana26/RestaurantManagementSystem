from django.contrib import admin

from .models import *

admin.site.register(UserData)
admin.site.register(FoodItem)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Payments)
admin.site.register(TableReservation)
admin.site.register(Reviews)
