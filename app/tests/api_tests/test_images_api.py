import httpx
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_proxy_image_success(mocker):
    fake_response = httpx.Response(
        status_code=200,
        content=b"fake-image-bytes",
        headers={"content-type": "image/png"},
    )

    async def fake_get(*args, **kwargs):
        return fake_response

    mocker.patch("httpx.AsyncClient.get", side_effect=fake_get)

    response = client.get("/images/proxy", params={"url": "http://example.com/test.png"})
    assert response.status_code == 200
    assert response.content == b"fake-image-bytes"
    assert response.headers["content-type"] == "image/png"


def test_proxy_image_connect_timeout(mocker):
    async def fake_get(*args, **kwargs):
        raise httpx.ConnectTimeout("timeout")

    mocker.patch("httpx.AsyncClient.get", side_effect=fake_get)

    response = client.get("/images/proxy", params={"url": "http://timeout-url"})
    assert response.status_code == 504
    assert "превышено время ожидания соединения" in response.text


def test_proxy_image_read_timeout(mocker):
    async def fake_get(*args, **kwargs):
        raise httpx.ReadTimeout("timeout")

    mocker.patch("httpx.AsyncClient.get", side_effect=fake_get)

    response = client.get("/images/proxy", params={"url": "http://slow-url"})
    assert response.status_code == 504
    assert "превышено время ожидания ответа сервера" in response.text


def test_proxy_image_error_status(mocker):
    fake_response = httpx.Response(status_code=404)

    async def fake_get(*args, **kwargs):
        return fake_response

    mocker.patch("httpx.AsyncClient.get", side_effect=fake_get)

    response = client.get("/images/proxy", params={"url": "http://not-found"})
    assert response.status_code == 404
    assert "Ошибка загрузки" in response.text
