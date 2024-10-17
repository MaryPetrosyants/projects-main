from fastapi import FastAPI
from router import router
from database import engine
import models
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router, prefix='/api', tags=['tasks'])


@app.get("/")
def root():
    return {"message": "API is running"}
