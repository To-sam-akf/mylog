from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from backend.database import ping_database
from backend.routers.health import router as health_router
from backend.routers.pages import router as pages_router
from backend.routers.auth import router as auth_router
from backend.routers.admin_pages import router as admin_pages_router
from backend.routers.upload import router as upload_router

from fastapi.staticfiles import StaticFiles



@asynccontextmanager
async def lifespan(app: FastAPI):
    ping_database()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(health_router)
app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(admin_pages_router)
app.include_router(upload_router)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def check_health():
    return {"status": "ok"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()

