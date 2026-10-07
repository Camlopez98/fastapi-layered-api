"""Tests de la capa API para el recurso /categories."""

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

CATEGORY = {"name": "Periféricos", "description": "Teclados, ratones y audífonos"}


async def _auth_headers(client: AsyncClient, user_payload: dict) -> dict:
    await client.post("/api/v1/auth/register", json=user_payload)
    login = await client.post(
        "/api/v1/auth/login",
        data={"username": user_payload["email"], "password": user_payload["password"]},
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


async def test_crud_completo_de_categorias(client: AsyncClient, user_payload: dict):
    headers = await _auth_headers(client, user_payload)

    creada = await client.post("/api/v1/categories/", json=CATEGORY, headers=headers)
    assert creada.status_code == 201
    category_id = creada.json()["id"]

    listado = await client.get("/api/v1/categories/")
    assert [c["id"] for c in listado.json()] == [category_id]

    actualizada = await client.put(
        f"/api/v1/categories/{category_id}", json={"is_active": False}, headers=headers
    )
    assert actualizada.status_code == 200
    assert actualizada.json()["is_active"] is False

    eliminada = await client.delete(f"/api/v1/categories/{category_id}", headers=headers)
    assert eliminada.status_code == 204

    no_existe = await client.get(f"/api/v1/categories/{category_id}")
    assert no_existe.status_code == 404


async def test_nombre_duplicado_responde_400(client: AsyncClient, user_payload: dict):
    headers = await _auth_headers(client, user_payload)
    await client.post("/api/v1/categories/", json=CATEGORY, headers=headers)

    repetida = await client.post("/api/v1/categories/", json=CATEGORY, headers=headers)
    assert repetida.status_code == 400


async def test_renombrar_a_un_nombre_existente_responde_400(client: AsyncClient, user_payload: dict):
    headers = await _auth_headers(client, user_payload)
    await client.post("/api/v1/categories/", json=CATEGORY, headers=headers)
    otra = await client.post("/api/v1/categories/", json={"name": "Monitores"}, headers=headers)

    response = await client.put(
        f"/api/v1/categories/{otra.json()['id']}", json={"name": CATEGORY["name"]}, headers=headers
    )
    assert response.status_code == 400


async def test_modificar_categorias_requiere_autenticacion(client: AsyncClient):
    response = await client.post("/api/v1/categories/", json=CATEGORY)
    assert response.status_code == 401
