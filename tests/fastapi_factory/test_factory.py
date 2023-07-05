import json
import math

from fastapi import FastAPI, Request, status
from fastapi.testclient import TestClient

from fastapi_factory.factory import (get_shared_object, set_exception_status,
                                     set_home, set_prometheus_exporter,
                                     set_shared_object)


def test_set_prometheus_exporter():
    app = FastAPI()
    set_prometheus_exporter(app)

    test_client = TestClient(app)
    response = test_client.get('/metrics')
    assert response.status_code == 200


def test_set_get_shared_object():
    app = FastAPI()

    # Set 'data' as the shared instance
    tag = 'data'
    data = {'foo', 'bar', 'foobar'}

    set_shared_object(app, data, tag)

    # Check if the element is in the set
    @app.get('/contains/{item}')
    async def contains(request: Request, item: str) -> bool:
        shared_data = get_shared_object(request, tag)
        return item in shared_data

    test_client = TestClient(app)
    assert test_client.get('/contains/foo').json() is True
    assert test_client.get('/contains/bar').json() is True
    assert test_client.get('/contains/unknown').json() is False

    # The instance is shared by reference
    data.remove('foo')
    assert test_client.get('/contains/foo').json() is False


def test_set_exception_status():
    app = FastAPI()

    # Returns the square root of numbers
    @app.get('/sqrt')
    async def get_sqrt_list(nums):
        nums = json.loads(nums)
        return [math.sqrt(n) for n in nums]

    set_exception_status(app, ValueError, status.HTTP_400_BAD_REQUEST)
    set_exception_status(app, TypeError, status.HTTP_406_NOT_ACCEPTABLE)

    test_client = TestClient(app)

    # Normal request
    response = test_client.get(
        '/sqrt',
        params={'nums': json.dumps([1, 4, 9])}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [1, 2, 3]

    # Negative numbers, should raise ValueError
    response = test_client.get(
        '/sqrt',
        params={'nums': json.dumps([-1, -4, -9])}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Array with string, should raise TypeError
    response = test_client.get(
        '/sqrt',
        params={'nums': json.dumps([1, 4, 'foo'])}
    )
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE


def test_set_home():
    title = 'test_home'
    version = '0.1.0'

    app = FastAPI(title=title, version=version)
    set_home(app)

    test_client = TestClient(app)
    response = test_client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': f'Hello from {title} {version}!'}
