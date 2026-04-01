from fastapi import FastAPI, HTTPException
import httpx
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI is starting up...")
    yield
    print("FastAPI is shutting down safely...")

app = FastAPI(lifespan=lifespan)

@app.post("/relay")
async def relay_data(data: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://localhost:8080/process-user", json=data)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Go service error: {str(e)}")

@app.get("/ping")
async def ping():
    return {"message": "pong"}
