from fastapi import FastAPI, HTTPException
import httpx
import os

POKEAPI_BASE_URL = os.getenv("POKEAPI_BASE_URL", "https://pokeapi.co/api/v2")

app = FastAPI(title="Pokemon Backend Service")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/pokemon")
async def list_pokemon(limit: int = 20, offset: int = 0):
    url = f"{POKEAPI_BASE_URL}/pokemon"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params={"limit": limit, "offset": offset}, timeout=10)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Error calling PokeAPI: {e}")
    data = resp.json()
    return {
        "count": data.get("count"),
        "results": [
            {
                "name": p["name"],
                "url": p["url"],
            }
            for p in data.get("results", [])
        ],
    }


@app.get("/pokemon/{name}")
async def get_pokemon(name: str):
    url = f"{POKEAPI_BASE_URL}/pokemon/{name}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=10)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Pokemon not found")
            raise HTTPException(status_code=502, detail=f"Error calling PokeAPI: {e}")
    data = resp.json()
    return {
        "id": data.get("id"),
        "name": data.get("name"),
        "height": data.get("height"),
        "weight": data.get("weight"),
        "sprites": data.get("sprites", {}).get("front_default"),
        "types": [t["type"]["name"] for t in data.get("types", [])],
    }

