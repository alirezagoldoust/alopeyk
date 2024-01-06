# Welcome to Alopeyk documentation
This project is API of [Alopeyk.com](https://alopeyk.com/) website
## How to use:
### Calculating the duration and cost from an origin to destination
```
/cost/origin=lat,long&destination=lat,long
```
It takes lat, long for both origin and destination in query prams of url, and returns duration in seconds and cost in tooman
\nexample:
```
http://127.0.0.1:8000/api/cost/?origin=35.75721789501081,2051.40967669493569&destination=35.746756453846,2051.37487729402636
```
