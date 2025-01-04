import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.data import dataRouter

load_dotenv()
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["Authorization"]
)

app.include_router(dataRouter)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8002)