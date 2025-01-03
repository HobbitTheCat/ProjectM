import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.users import userRouter
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["Authorization"]
)

app.include_router(userRouter)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
