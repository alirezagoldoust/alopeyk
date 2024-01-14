from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializer import UserSerializer, GroupSerializer, ProfileSerializer, OrderSerializer, FeedbackSerializer
from .models import ApiKey, Order, Feedback
from .permissions import IsDriver, IsCustomer, IsCustomerOrDriver
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


def calculate_cost(origin, destination):
    duration = find_duration(origin, destination)
    cost_per_hour = 200000
    cost = (duration / 3600) * cost_per_hour
    cost = cost * 1.02 if is_holyday() else cost
    return int(cost)

class Price(APIView):
    # authentication_classes = [JWTAuthentication]
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
        cost = calculate_cost(origin, destination)
        return Response({'price':cost, 'duration':str(datetime.timedelta(seconds=int(duration)))})


class Signup(APIView):
    # This view will perform signup
    def post(self, request):
        data = request.data
        if not data.get('groups'):
            data['groups'] = [1]
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            if len(data['groups']) != 1:
                return Response('The user should belong to one group!')
            if data['groups'][0] > 2:
                return Response({"groups":"invalid group id"})
            user = serializer.save()

            # updating saved raw password to hashed password
            user.set_password(user.password)
            user.save()

            # making profile for user
            data['user'] = user.id
            serializer = ProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                user.delete()
                return Response(serializer.errors)

            # generating token
            refresh_token = RefreshToken.for_user(user)
            RefreshToken.set_exp(refresh_token, from_time=datetime.datetime.now(), 
                                lifetime=datetime.timedelta(days=15))

            # returning response
            return Response({
                'message': 'User successfully created',
                'access token':str(refresh_token.access_token),
                'refresh token':str(refresh_token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupsList(generics.ListAPIView):
    # returns the name and id of all groups of users
    queryset = Group.objects.exclude(name__in=['Driver', 'Admin'])
    serializer_class = GroupSerializer


class AddOrder(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    def post(self, request):

        # Checking data validation and existance of previous order
        data = request.data
        if len(data.get('origin', [])) != 2:
            return Response({'Origin':'This field should be a list of lat, long'})
        if len(data.get('destination', [])) != 2:
            return Response({'destination':'This field should be a list of lat, long'})
        if not is_tehran(data['origin']) or not is_tehran(data['destination']):
            return Response('The origin or destination is not in Tehran!')
        if Order.objects.filter(customer=request.user, status__in=['0', '1', '2']).count():
            return Response('You have an existing order! please finish or cancel it to add new one')
        
        # completing data
        data['cost'] = calculate_cost(data['origin'], data['destination'])
        duration = find_duration(data['origin'], data['destination'])
        if data.get('has_return', False):
            duration += find_duration(data['destination'], data['origin'])
            data['cost'] += calculate_cost(data['destination'], data['origin'])
        duration = str(datetime.timedelta(seconds=int(duration)))
        data['duration'] = duration
        data['customer'] = request.user.id
        data['origin'] = ','.join(data['origin'])
        data['destination'] = ','.join(data['destination'])

        # saving data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response('Order succesfully created!', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class CancelOrder(APIView):
    permission_classes = [IsAuthenticated, IsCustomerOrDriver]
    def delete(self, request):
        # the view automatically finds out the the user is customer or driver and cancels corresponding order, so it's a bit dirty :\
        if request.user.groups.all()[0].name == 'Customer':
            try:
                order = Order.objects.get(customer=request.user, status='0')
                order.status = '-1'
                order.save()
                return Response("The order successfully canceled")
            except:
                try:
                    order = Order.objects.get(customer=request.user, status__in=['1', '2', '3'])
                    return Response("You can't cancel in process order!")
                except:
                    return Response("You don't have any active order!")
        else:
            try:
                order = Order.objects.get(driver=request.user, status__in=['0', '1', '2'])
                order.status = '-2'
                order.save()
                return Response("The order successfully canceled")
            except:
                try:
                    order = Order.objects.get(customer=request.user, status__in=['1', '2', '3'])
                    return Response("You can't cancel in process order!")
                except:
                    return Response("You don't have any active order!")


class MyOrder(APIView):
    permission_classes = [IsAuthenticated, IsCustomerOrDriver]
    def get(self, request): 
        is_active = request.GET.get('active')
        status_list = ['0', '1', '2', '3', '-1', '-2']

        # returns all of the orders of a user and the active one if the 'active=true' comes in query prams
        if is_active == 'true':
            status_list = status_list[:3]
        if request.user.groups.all()[0].name == 'Customer':
            try:
                return Response(OrderSerializer(Order.objects.filter(customer=request.user, status__in=status_list).order_by('-status'), many=True).data)
            except:
                return Response("You don't have any active order!")
        else:
            try:
                return Response(OrderSerializer(Order.objects.filter(driver=request.user, status__in=status_list).order_by('-status'), many=True).data)
            except:
                return Response("You don't have any active order!")

class FeedbackView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class OrderList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsDriver]
    queryset = Order.objects.filter(status='0')
    serializer_class = OrderSerializer