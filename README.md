# HyperText Transfer Protocol, Python implementation

[HttPy](https://github.com/mahtat555/HttPy) is a package that collects several
modules for working with the HyperText Transfer Protocol:

**This implementation is written in python 3**

At the end of this small project, this package that we are going to create will have three main functions:

1. Send a request and receive a response from an HTTP server, with the `client` module
2. Create an HTTP server, with the `server` module
3. Handled cookies, with the `cookie` module

## Install

```sh
$ git clone https://github.com/mahtat555/HttPy.git
$ cd HttPy/
$ python setup.py install
```

## Usage

### 1. The `client` module

#### Examples of usage

#### Example 1

```python
>>> from httpy import AsyncRequest
>>> r = AsyncRequest(method="GET", url="https://reqres.in/api/users")
>>> res = r.fetch_run()
>>> res.statuscode
200
>>> res.statusmessage
'OK'
>>> res.version
'HTTP/1.1'
>>> res.headers
{'Date': 'Sun, 14 Feb 2021 17:19:17 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': '996', 'Connection': 'close', 'Set-Cookie': '__cfduid=d5e240ad012e2e501e4343d86c1dc2d281613323157; expires=Tue, 16-Mar-21 17:19:17 GMT; path=/; domain=.reqres.in; HttpOnly; SameSite=Lax; Secure', 'X-Powered-By': 'Express', 'Access-Control-Allow-Origin': '*', 'Etag': 'W/"3e4-2RLXvr5wTg9YQ6aH95CkYoFNuO8"', 'Via': '1.1 vegur', 'Cache-Control': 'max-age=14400', 'CF-Cache-Status': 'HIT', 'Age': '6462', 'Accept-Ranges': 'bytes', 'cf-request-id': '084326d82f0000371b4d2a6000000001', 'Expect-CT': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"', 'Report-To': '{"group":"cf-nel","endpoints":[{"url":"https:\\/\\/a.nel.cloudflare.com\\/report?s=NeoAHS26CtMYVCuzWrZolvjn7M6NPvWUvf3USEj2ap%2BRv3LJZwWHgP1ae3wyve1cx3KKc7xEMTLdiWAeuIUlliDxm27ibcNF%2B18%3D"}],"max_age":604800}', 'NEL': '{"max_age":604800,"report_to":"cf-nel"}', 'Server': 'cloudflare', 'CF-RAY': '62187406bbdb371b-MIA'}
>>> res.body
b'{"page":1,"per_page":6,"total":12,"total_pages":2,"data":[{"id":1,"email":"george.bluth@reqres.in","first_name":"George","last_name":"Bluth","avatar":"https://reqres.in/img/faces/1-image.jpg"},{"id":2,"email":"janet.weaver@reqres.in","first_name":"Janet","last_name":"Weaver","avatar":"https://reqres.in/img/faces/2-image.jpg"},{"id":3,"email":"emma.wong@reqres.in","first_name":"Emma","last_name":"Wong","avatar":"https://reqres.in/img/faces/3-image.jpg"},{"id":4,"email":"eve.holt@reqres.in","first_name":"Eve","last_name":"Holt","avatar":"https://reqres.in/img/faces/4-image.jpg"},{"id":5,"email":"charles.morris@reqres.in","first_name":"Charles","last_name":"Morris","avatar":"https://reqres.in/img/faces/5-image.jpg"},{"id":6,"email":"tracey.ramos@reqres.in","first_name":"Tracey","last_name":"Ramos","avatar":"https://reqres.in/img/faces/6-image.jpg"}],"support":{"url":"https://reqres.in/#support-heading","text":"To keep ReqRes free, contributions towards server costs are appreciated!"}}'
>>> res.json()
{'page': 1, 'per_page': 6, 'total': 12, 'total_pages': 2, 'data': [{'id': 1, 'email': 'george.bluth@reqres.in', 'first_name': 'George', 'last_name': 'Bluth', 'avatar': 'https://reqres.in/img/faces/1-image.jpg'}, {'id': 2, 'email': 'janet.weaver@reqres.in', 'first_name': 'Janet', 'last_name': 'Weaver', 'avatar': 'https://reqres.in/img/faces/2-image.jpg'}, {'id': 3, 'email': 'emma.wong@reqres.in', 'first_name': 'Emma', 'last_name': 'Wong', 'avatar': 'https://reqres.in/img/faces/3-image.jpg'}, {'id': 4, 'email': 'eve.holt@reqres.in', 'first_name': 'Eve', 'last_name': 'Holt', 'avatar': 'https://reqres.in/img/faces/4-image.jpg'}, {'id': 5, 'email': 'charles.morris@reqres.in', 'first_name': 'Charles', 'last_name': 'Morris', 'avatar': 'https://reqres.in/img/faces/5-image.jpg'}, {'id': 6, 'email': 'tracey.ramos@reqres.in', 'first_name': 'Tracey', 'last_name': 'Ramos', 'avatar': 'https://reqres.in/img/faces/6-image.jpg'}], 'support': {'url': 'https://reqres.in/#support-heading', 'text': 'To keep ReqRes free, contributions towards server costs are appreciated!'}}
>>>
```

#### Example 2

- The method `GET` with the `params`

```python
>>> from httpy import get
>>>
>>> r = get(
...     "https://httpbin.org/get",
...     params={"param1": "value1", "param2": "value2"}
... )
>>> r
<Response [200]>
>>> r.headers["Content-Type"]
'application/json'
>>> json = r.json()
>>> json["args"]
{'param1': 'value1', 'param2': 'value2'}
>>>
```

- The method `POST` with the `json`

```python
>>> from httpy import post
>>>
>>> r = post(
...     "https://httpbin.org/post",
...     json={"name": "Mahtat", "age": 26, "languages": ["python", "js"]}
... )
>>> r.statuscode
200
>>> r.headers["Content-Type"]
'application/json'
>>> json = r.json()
>>> json['data']
'{"name": "Mahtat", "age": 26, "languages": ["python", "js"]}'
>>> json['json']
{'age': 26, 'languages': ['python', 'js'], 'name': 'Mahtat'}
>>>
```

- The method `POST` with the `form`

```python
>>> from httpy import post
>>>
>>> r = post(
...     "https://httpbin.org/post",
...     data={"Anime": "Violet Evergarden", "episode": 12}
... )
>>> r.statuscode
200
>>> r.headers["Content-Type"]
'application/json'
>>> json = r.json()
>>> json['form']
{'Anime': 'Violet Evergarden', 'episode': '12'}
>>>
```

#### Example 3

**Synchronous and asynchronous requests**
