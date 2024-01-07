# Welcome to Alopeyk documentation
This project is API of [Alopeyk.com](https://alopeyk.com/) website
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
}
```
group key is primary key of the group that the new user belongs to. the list of role groups is acesssable in:
```
/api/groups/
```
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
### Calculating the duration and cost from an origin to destination
<br>It takes lat, long for both origin and destination in query prams of url, and returns duration in seconds and cost in tooman. note that this request needs authentication
```
api/cost/origin=lat,long&destination=lat,long
```
Both the origin and destination should be in Tehran, example:
```
http://127.0.0.1:8000/api/cost/?origin=35.75721789501081,2051.40967669493569&destination=35.746756453846,2051.37487729402636
```
