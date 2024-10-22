from fastapi import FastAPI
from routers import user_router
from routers import router


from config.database import engine
import models.models as models
import models.user as models_user

models.Base.metadata.create_all(bind=engine)
models_user.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router.router )
app.include_router(user_router.router)


@app.get("/")
def root():
    return {"message": "API is running"}
