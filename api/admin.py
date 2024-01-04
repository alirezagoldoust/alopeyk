from django.contrib.admin import register, ModelAdmin
from .models import ApiKey

@register(ApiKey)
class ApiAdmin(ModelAdmin):
    pass 

