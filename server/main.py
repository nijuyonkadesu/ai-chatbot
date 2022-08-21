from fastapi import FastAPI, Request
import uvicorn
import os
from dotenv import load_dotenv
from src.routes import chat
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

api = FastAPI()
# https://stackoverflow.com/questions/59965872/how-to-solve-no-attribute-routes-in-fastapi
api.include_router(chat.chat)
origins = ["http://localhost:3000"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type"]
)

@api.get("/test")
async def root():
    return {"msg": "api is online"}

if __name__ == "__main__":
    if os.environ.get('APP_ENV') == "development":
        uvicorn.run("main:api", host="0.0.0.0", port=3500,
        workers=4, reload=True)
    else:
        pass