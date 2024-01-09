from django.urls import path
from .views import Price, Signup, GroupsList
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns=[
    path('cost/', Price.as_view()),
    path('signup/', Signup.as_view()),
    path('groups/', GroupsList.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]