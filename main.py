from fastapi import FastAPI
from routes.anmat import anmat

app = FastAPI()

app.include_router(anmat)