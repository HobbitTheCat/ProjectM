import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes.user import userRouter

load_dotenv()

app = FastAPI()
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