# FastAPI-Factory

Some simple utilities for building `FastAPI` application.

## Installation
Install via `pip`
```bash
pip install git+https://github.com/Pandede/fastapi-factory
```

## Usage
### Exports the metrics to `Prometheus`
```python
from fastapi import FastAPI
from fastapi_factory import set_prometheus_exporter


app = FastAPI()
set_prometheus_exporter(app)
```

### Add a shared instance across the application

The instance can be accessed in endpoints or middlewares with attribute `request`.

For example, assume `redis.Redis` is going to be shared across the application, in `main.py`:
```python
from fastapi import FastAPI
from fastapi_factory import set_shared_object
from redis import Redis

from routers import user_router
app = FastAPI()

# Share `redis.Redis`
redis_client = Redis()
set_shared_object(app, redis_client, 'redis')
```
Then, access the shared instance in the endpoint, in `routers.py`:
```python
from fastapi import APIRouter, Request
from fastapi_factory import get_shared_object

user_router = APIRouter()

@user_router.get('/user')
def get_info(request: Request, user: str) -> str:
    redis_client = get_shared_object(request, 'redis')
    return redis_client.get(user)

@user_router.post('/user')
def set_info(request: Request, user: str, info: str):
    redis_client = get_shared_object(request, 'redis')
    return redis_client.set(user, info)
```

### Catch the exception with specific status code
```python
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from fastapi_factory import set_exception_status

app = FastAPI()
set_exception_status(app, ZeroDivisionError, status.HTTP_400_BAD_REQUEST)
set_exception_status(app, ValueError, status.HTTP_406_NOT_ACCEPTABLE)


@app.get('/inv')
def get_inv(n):
    if n == 'nan':
        raise TypeError('nan')
    return 1 / float(n)


test_client = TestClient(app, raise_server_exceptions=False)

# Normal request
res = test_client.get('/inv', params={'n': 4})
assert res.status_code == status.HTTP_200_OK
assert res.json() == 0.25

# Zero, must raise ZeroDivisionError
res_with_zero_div = test_client.get('/inv', params={'n': 0})
assert res_with_zero_div.status_code == status.HTTP_400_BAD_REQUEST

# String, must raise ValueError
res_with_val_err = test_client.get('/inv', params={'n': 'foo'})
assert res_with_val_err.status_code == status.HTTP_406_NOT_ACCEPTABLE
assert res_with_val_err.json() == {'detail': 'could not convert string to float: \'foo\''}

# nan, must raise TypeError
# Returns 500 as it's unexpected error
res_with_type_err = test_client.get('/inv', params={'n': 'nan'})
assert res_with_type_err.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
```

### Create a simple homepage
```python
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from fastapi_factory import set_home

app = FastAPI(title='fastapi_factory', version='0.1.0')
set_home(app)

test_client = TestClient(app)
res = test_client.get('/')
assert res.status_code == status.HTTP_200_OK
assert res.json() == {'message': 'Hello from fastapi_factory 0.1.0!'}
```

## Test
Install the following packages before testing:
```bash
pip install pytest pytest-cov pytest-mock
```
Executing the tests:
```bash
python3 -m pytest tests --cov
```