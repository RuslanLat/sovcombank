from typing import Optional, Dict
from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from app.admin.models import Admin
from app.users.models import User
from app.store import Store, setup_store
from app.store.database.database import Database
from app.web.config import Config, setup_config
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes


class Application(AiohttpApplication):
    config: Optional[Config] = None
    store: Optional[Store] = None
    database: Optional[Database] = None


class Request(AiohttpRequest):
    user: dict
    admin: Optional[Admin] = None
    user: Optional[User] = None

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def database(self):
        return self.request.app.database

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})


app = Application()

description = """

TO DO API

Сервис автоматического распределения задач для выездных сотрудников банка.
Система автоматического распределения задач на рабочую неделю
с построением оптимального маршрута посещения объектов сотрудником банка.


## Разработчик

* Руслан Латипов, @rus_lat116

"""

tags_metadata = [
    {
        "name": "admin",
        "description": "Аутентификация админа",
    },
    {
        "name": "users",
        "description": "Добавление/удаление пользователей",
    },
    {
        "name": "ranks",
        "description": "Добавление/удаление грейда",
    },
    {
        "name": "positions",
        "description": "Добавление/удаление должностей",
    },
    {
        "name": "jobs",
        "description": "Добавление/удаление работников в штат",
    },
    {
        "name": "todo",
        "description": "Обработка задач",
    },
    {
        "name": "problems",
        "description": "Добавление/удаление задач",
    },
    {
        "name": "partners",
        "description": "Добавление/удаление партнёров",
    },
    {
        "name": "addresses",
        "description": "Добавление/удаление адресов",
    },
    {
        "name": "offices",
        "description": "Добавление/удаление филиалов",
    },
     {
        "name": "partner_params",
        "description": "Добавление/удаление критериев партнёра",
    },
]


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    session_setup(app, EncryptedCookieStorage(app.config.session.key))
    setup_routes(app)
    setup_aiohttp_apispec(
        app,
        title="TO DO API",
        version="0.0.1",
        swagger_path="/docs",
        url="/docs/json",
        info=dict(
            description=description,
            contact={
                "name": "Руслан Латипов",
                "url": "https://t.me/rus_lat116",
                "email": "rus_kadr03@mail.ru",
            },
        ),
        tags=tags_metadata,
    )
    setup_middlewares(app)
    setup_store(app)


    
    return app
