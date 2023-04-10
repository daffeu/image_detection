from db.base import Base
from auth.routes import router as auth_router
from main.routes import router as main_router
from fastapi import FastAPI
from db.utils import check_db_connected, check_db_disconnected
from db.session import engine


def include_router(app):
    app.include_router(auth_router, prefix="", tags=["auth"])
    app.include_router(main_router, prefix="", tags=["main"])


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI()
    include_router(app)
    create_tables()
    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
