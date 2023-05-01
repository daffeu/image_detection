from auth.routes import router as auth_router
from main.routes import router as main_router
from fastapi import FastAPI


def include_router(app):
    app.include_router(auth_router, prefix="", tags=["auth"])
    app.include_router(main_router, prefix="", tags=["main"])


def start_application():
    app = FastAPI()
    include_router(app)
    return app


app = start_application()