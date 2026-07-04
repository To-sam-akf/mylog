from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from backend.database import ping_database
from backend.routers.health import router as health_router
from backend.routers.pages import router as pages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    ping_database()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(pages_router)

@app.get("/")
def check_health():
    return {"status": "ok"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()

