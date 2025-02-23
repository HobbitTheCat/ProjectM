from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.postgres import engineA
from database.redis import create_redis_pool, close_redis_pool
from sqlmodel import SQLModel, Session
from sqlalchemy import text
from routes.user import userRouter

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engineA)
    with Session(engineA) as session:
        session.execute(text("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO acs_service;"))
        session.execute(text("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO acs_service;"))
        session.commit()
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)