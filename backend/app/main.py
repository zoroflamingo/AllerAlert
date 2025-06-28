from fastapi import FastAPI
from .routers import dishes_router, allergens_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API is up and running"}


app.include_router(dishes_router)
app.include_router(allergens_router)
