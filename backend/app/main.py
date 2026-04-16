from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.routers.auth import router as auth_router

app = FastAPI(title="Ecommerce Backend", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Ecommerce backend is running"}