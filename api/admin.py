from django.contrib import admin
from .models import Profile, Order, Feedback

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('posting_time',)

admin.site.register(Profile)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback)

