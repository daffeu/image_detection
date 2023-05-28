from auth.routes import router as auth_router
from main.routes import router as main_router
from fastapi import FastAPI
from consumer.subscriptions import consumer_subscriptions
import asyncio


def include_router(app):
    app.include_router(auth_router, prefix="", tags=["auth"])
    app.include_router(main_router, prefix="", tags=["main"])


def start_application():
    app = FastAPI()
    loop = asyncio.get_event_loop()
    loop.create_task(consumer_subscriptions())
    include_router(app)
    return app


app = start_application()
