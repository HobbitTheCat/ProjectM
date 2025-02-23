import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.user import userRouter
from routes.auth import userAuthRouter
from routes.schedule import scheduleRouter
from database.redis import create_redis_pool, close_redis_pool

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_redis_pool()
    yield
    await close_redis_pool()

app = FastAPI(lifespan=lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(userRouter)
app.include_router(userAuthRouter)
app.include_router(scheduleRouter)

from starlette.responses import Response

@app.options("/{full_path:path}")
async def preflight(full_path: str):
    return Response(status_code=204, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, accept",
    })

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8010)
