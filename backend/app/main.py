from fastapi import FastAPI
from app.routers.dish import dishes_router
from app.routers.allergen import allergens_router
from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is up and running"}


app.include_router(dishes_router)
app.include_router(allergens_router)
