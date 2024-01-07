from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializer import UserSerializer, GroupSerializer
from .models import ApiKey
from .permissions import IsDriver
import requests
import datetime

def is_tehran(location):
    lat = location[0]
    long = location[1]
    url = f'https://api.neshan.org/v5/reverse?lat={lat}&lng={long}'
    api_key = ApiKey.objects.get(name='admin').apikey   
    city = (requests.get(headers={'Api-key' : api_key}, url=url)).json()['city']
    if city == 'تهران':
        return True
    return False


def find_duration(origin, destination):
    # This view takes origin and destination and returns the duration in seconds
    url = f'https://api.neshan.org/v4/direction?origin={origin[0]},{origin[1]}&destination={destination[0]},{destination[1]}&type=motorcycle'
    api_key = ApiKey.objects.get(name='admin').apikey   
    duration = (requests.get(headers={'Api-key' : api_key}, url=url)).json()['routes'][0]['legs'][0]['duration']['value']
    return duration


def is_holyday():
    today = datetime.date.today()
    url = f'https://holidayapi.ir/gregorian/{today.year}/{today.month}/{today.day}'
    return requests.get(url).json()['is_holiday']


def calculate_cost(duration):
    cost_per_hour = 200000
    cost = (duration / 3600) * cost_per_hour
    cost = cost * 1.02 if is_holyday() else cost
    return int(cost)

class Price(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # This view calculate duration from origin to destination
    def get(self, request):
        # Getting latitude and longitude from query prameters
        try:
            origin = list(map(float, request.GET.get('origin').split(',')))
            destination = list(map(float, request.GET.get('destination').split(',')))
        except:
            return Response('origin or destination not valid!')
        if not is_tehran(origin) or not is_tehran(destination):
            return Response('The origin or destination is not in Tehran!')
        duration = find_duration(origin, destination)
        cost = calculate_cost(duration)
        return Response({'price':cost})


class Signup(APIView):
    # This view will perform signup
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # updating saved raw password to hashed password
            user = User.objects.get(username=request.data['username'])
            user.set_password(user.password)
            user.save()

            # generating token
            access_token = str(AccessToken.for_user(user))
            refresh_token = str(RefreshToken.for_user(user))

            # returning response
            return Response({
                'message': 'User successfully created',
                'access token':access_token, 
                'refresh token':refresh_token, 
                'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    # This view will perform login, it takes username and password and returns the token if it was correct
    def post(self, request):

        # Checking user existance
        try:
            user = User.objects.get(username=request.data['username'])
        except:
            return Response("username does not exist", status=status.HTTP_404_NOT_FOUND)
            
        # Checking password
        if not user.check_password(request.data['password']):
            return Response("wrong password", status=status.HTTP_400_BAD_REQUEST)

        # Generating token
        access_token = str(AccessToken.for_user(user))
        refresh_token = str(RefreshToken.for_user(user))
        return Response({'message': 'Successfully logged in', 
                         'access token':access_token, 
                         'refresh token':refresh_token})

class GroupsList(generics.ListAPIView):
    # returns the name and id of all groups of users
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

