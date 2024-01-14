# Welcome to Alopeyk documentation
This project is API of [Alopeyk.com](https://alopeyk.com/) website
please turn off your VPN befor use!
## How to use:
### Creating account
you should give a username, password, group_id(defualt is 1 = Customer, and 2 = Driver_applied) in request body, then it returns a token
```
(post):api/signup/

body:
{
  username='username'
  password='password'
  groups = [group_id]
  phone_number = 'phone_number'
}
```
group key is primary key of the group that the new user belongs to. the list of role groups is acesssable in:
```
(get):/api/groups/
```
age, email and sex(f/m) are optional<br>
driver applied users become Driver when admins accept their apply
### Login
you can take token of the you user if lost with entering username and password in request body
```
(post):api/login

body:
{
  username='username'
  password='password'
}

```
### Refresh Token
```
(post):api/token/refresh
```
### Verify Token
```
(post):api/token/verify
```
### Calculating the duration and cost from an origin to destination
<br>It takes lat, long for both origin and destination in query prams of url, and returns duration time and cost in tooman. note that this request needs authentication
```
(get):api/cost/origin=lat,long&destination=lat,long
```
Both the origin and destination should be in Tehran, example:
```
http://127.0.0.1:8000/api/cost/?origin=35.75721789501081,2051.40967669493569&destination=35.746756453846,2051.37487729402636
```
### Adding order
this request requires Athentication, and the user should be a customer. Each user can have only one order at the time.
```
(post):api/order/add
body:
{
    "origin" : ["35.75019411613506", "51.28322697712252"],
    "destination" : ["35.73156544666984", "51.381008953539585"]
}
```
description, has_return are optional
### My orders
this request requires Athentication, returns all of your orders
```
(get):api/order/
```
if you pass query parameter 'active=true' it returns only the active order
### Cancel order
this request requires Athentication, customers and drivers can cancel their active order and shows the active order if exist.
```
(del):api/order/cancel/
```
### Give feedback
this request requires Athentication, customers can give the order id and their score(0-5)
```
(post):api/order/feedback/
body:
{
    "order" : 2,
    "rate" : 4
}
```
<br> you can get id of a order in previous request
### Order list
this request requires Athentication, drivers can see open orders from customers sorted by their distance.
```
(get):api/order/list/
body:
{
    "position" : [lat, long]
}
```
