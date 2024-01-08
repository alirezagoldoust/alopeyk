from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
