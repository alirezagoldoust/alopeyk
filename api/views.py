from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
# from rest_framework.request import Request
from rest_framework.response import Response
from .models import ApiKey
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
        return Response({'price of peyk (in tooman)':cost})


