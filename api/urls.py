from django.urls import path
from .views import Price, Signup, GroupsList, Login

urlpatterns=[
    path('cost/', Price.as_view()),
    path('signup/', Signup.as_view()),
    path('login/', Login.as_view()),
    path('groups/', GroupsList.as_view()),
]