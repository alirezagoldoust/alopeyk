from django.urls import path
from .views import is_tehran, Price

urlpatterns=[
    path('', Price.as_view())
]