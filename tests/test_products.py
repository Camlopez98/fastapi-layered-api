"""Tests de la capa API para el recurso /products."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

PRODUCT = {"name": "Teclado", "description": "Mecánico", "price": 150000, "is_available": True}


async def _auth_headers(client: AsyncClient, user_payload: dict) -> dict:
    await client.post("/api/v1/auth/register", json=user_payload)
    login = await client.post(
        "/api/v1/auth/login",
        data={"username": user_payload["email"], "password": user_payload["password"]},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


async def test_crud_completo_de_productos(client: AsyncClient, user_payload: dict):
    headers = await _auth_headers(client, user_payload)

    creado = await client.post("/api/v1/products/", json=PRODUCT, headers=headers)
    assert creado.status_code == 201
    product_id = creado.json()["id"]

    listado = await client.get("/api/v1/products/")
    assert listado.status_code == 200
    assert [p["id"] for p in listado.json()] == [product_id]

    actualizado = await client.put(
        f"/api/v1/products/{product_id}", json={"price": 120000}, headers=headers
    )
    assert actualizado.status_code == 200
    assert actualizado.json()["price"] == 120000
    assert actualizado.json()["name"] == "Teclado"

    eliminado = await client.delete(f"/api/v1/products/{product_id}", headers=headers)
    assert eliminado.status_code == 204

    no_existe = await client.get(f"/api/v1/products/{product_id}")
    assert no_existe.status_code == 404


async def test_precio_negativo_responde_400(client: AsyncClient, user_payload: dict):
    headers = await _auth_headers(client, user_payload)
    response = await client.post(
        "/api/v1/products/", json={**PRODUCT, "price": -1}, headers=headers
    )
    assert response.status_code == 400


async def test_modificar_productos_requiere_autenticacion(client: AsyncClient):
    response = await client.post("/api/v1/products/", json=PRODUCT)
    assert response.status_code == 401
