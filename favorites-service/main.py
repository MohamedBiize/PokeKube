from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import os
import sqlalchemy
from sqlalchemy import text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pokemon:pokemon_password@localhost:5432/pokemon_favorites",
)

engine = sqlalchemy.create_engine(DATABASE_URL, future=True)

app = FastAPI(title="Pokemon Favorites Service")


def init_db():
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS favorites (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    pokemon_name VARCHAR(100) NOT NULL
                );
                """
            )
        )


@app.on_event("startup")
def on_startup():
    init_db()


class FavoriteIn(BaseModel):
    username: str
    pokemon_name: str


class FavoriteOut(BaseModel):
    id: int
    username: str
    pokemon_name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/favorites", response_model=FavoriteOut)
def add_favorite(fav: FavoriteIn):
    with engine.begin() as conn:
        result = conn.execute(
            text(
                """
                INSERT INTO favorites (username, pokemon_name)
                VALUES (:username, :pokemon_name)
                RETURNING id, username, pokemon_name;
                """
            ),
            {"username": fav.username, "pokemon_name": fav.pokemon_name},
        )
        row = result.fetchone()
        if not row:
            raise HTTPException(status_code=500, detail="Failed to insert favorite")
        return FavoriteOut(id=row.id, username=row.username, pokemon_name=row.pokemon_name)


@app.get("/favorites/{username}", response_model=List[FavoriteOut])
def list_favorites(username: str):
    with engine.begin() as conn:
        result = conn.execute(
            text(
                """
                SELECT id, username, pokemon_name
                FROM favorites
                WHERE username = :username
                ORDER BY id DESC;
                """
            ),
            {"username": username},
        )
        rows = result.fetchall()
        return [
            FavoriteOut(id=row.id, username=row.username, pokemon_name=row.pokemon_name)
            for row in rows
        ]


@app.get("/leaderboard")
def leaderboard(limit: int = 10):
    with engine.begin() as conn:
        result = conn.execute(
            text(
                """
                SELECT pokemon_name, COUNT(*) AS favorites_count
                FROM favorites
                GROUP BY pokemon_name
                ORDER BY favorites_count DESC
                LIMIT :limit;
                """
            ),
            {"limit": limit},
        )
        rows = result.fetchall()
        return [
            {"pokemon_name": row.pokemon_name, "favorites_count": row.favorites_count}
            for row in rows
        ]

