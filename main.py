from fastapi import FastAPI
from routes.anmat import anmat
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(anmat)