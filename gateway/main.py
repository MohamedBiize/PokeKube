from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
FAVORITES_URL = os.getenv("FAVORITES_URL", "http://favorites-service:8001")

app = FastAPI(title="Pokemon Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/pokemon")
async def list_pokemon(limit: int = 20, offset: int = 0):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{BACKEND_URL}/pokemon", params={"limit": limit, "offset": offset})
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting backend: {e}")
    return resp.json()


@app.get("/pokemon/{name}")
async def get_pokemon(name: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{BACKEND_URL}/pokemon/{name}")
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting backend: {e}")
    return resp.json()


@app.post("/favorites")
async def add_favorite(username: str, pokemon_name: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{FAVORITES_URL}/favorites", json={"username": username, "pokemon_name": pokemon_name}
            )
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting favorites-service: {e}")
    return resp.json()


@app.get("/favorites/{username}")
async def list_favorites(username: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{FAVORITES_URL}/favorites/{username}")
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting favorites-service: {e}")
    return resp.json()


@app.get("/leaderboard")
async def leaderboard(limit: int = 10):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{FAVORITES_URL}/leaderboard", params={"limit": limit})
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting favorites-service: {e}")
    return resp.json()

