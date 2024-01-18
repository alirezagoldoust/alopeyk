from django.urls import path
from .views import (Price, Signup, GroupsList, AddOrder, CancelOrder, 
                    MyOrder, FeedbackView, OrderList, AcceptOrder,
                    TookStuff, DeliverOrder, AverageFeedbackScore)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns=[
    path('cost/', Price.as_view()),
    path('groups/', GroupsList.as_view()),
    path('signup/', Signup.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('order/', MyOrder.as_view()),
    path('order/add/', AddOrder.as_view()),
    path('order/cancel/', CancelOrder.as_view()),
    path('order/feedback/', FeedbackView.as_view()),
    path('order/list/', OrderList.as_view()),
    path('order/accept/<int:pk>', AcceptOrder.as_view()),
    path('order/tookstuff/', TookStuff.as_view()),
    path('order/delivered/', DeliverOrder.as_view()),
    path('order/delivered/', DeliverOrder.as_view()),
    path('avgscore/', AverageFeedbackScore.as_view()),
]