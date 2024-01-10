# Welcome to Alopeyk documentation
This project is API of [Alopeyk.com](https://alopeyk.com/) website
please turn off your VPN befor use!
## How to use:
### Creating account
you should give a username, password, group_id in requeset body, then it returns a token
```
api/signup/

body:
{
  username='username'
  password='password'
  group = [group_id]
  phone_number = 'phone_number'
}
```
group key is primary key of the group that the new user belongs to. the list of role groups is acesssable in:
```
/api/groups/
```
age, email and sex(f/m) are optional<br>
### Login
you can take token of the you user if lost with entering username and password in request body
```
api/login

body:
{
  username='username'
  password='password'
}

```
### Refresh Token
```
api/token/refresh
```
### Verify Token
```
api/token/verify
```
### Calculating the duration and cost from an origin to destination
<br>It takes lat, long for both origin and destination in query prams of url, and returns duration time and cost in tooman. note that this request needs authentication
```
api/cost/origin=lat,long&destination=lat,long
```
Both the origin and destination should be in Tehran, example:
```
http://127.0.0.1:8000/api/cost/?origin=35.75721789501081,2051.40967669493569&destination=35.746756453846,2051.37487729402636
```
### Adding order
this request requires Athentication, and the user should be a customer. Each user can have only one order at the time.
```
api/addorder
body:
{
    "origin" : ["35.75019411613506", "51.28322697712252"],
    "destination" : ["35.73156544666984", "51.381008953539585"]
}
```
description is optional
