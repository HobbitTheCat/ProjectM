import uvicorn
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlmodel import SQLModel, Session
from database import engineA
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes.user import userRouter

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engineA)
    with Session(engineA) as session:
        session.execute(text("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO acs_service;"))
        session.execute(text("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO acs_service;"))
        session.commit()
    yield

app = FastAPI(lifespan=lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Authorization"]
)

app.include_router(userRouter)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)