from fastapi import FastAPI
from app.routers import dish, allergen
from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is up and running"}


app.include_router(dish.router)
app.include_router(allergen.router)
