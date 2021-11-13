from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_context.middleware import RawContextMiddleware
from starlette_context.plugins.base import Plugin

from errors import NinjaError
from i18n import gettext as _
from i18n import lazy_gettext as _l


class AcceptLanguagesHeaderPlugin(Plugin):
    key = "Accept-Languages"


middleware = [
    Middleware(
        RawContextMiddleware,
        plugins=(AcceptLanguagesHeaderPlugin(),),
    )
]

app = FastAPI(middleware=middleware)


class NinjaException(Exception):
    ...


class LazyNinjaException(Exception):
    ...


@app.exception_handler(NinjaException)
async def ninja_exception_handler(request: Request, exc: NinjaException):
    return JSONResponse(
        status_code=418,
        # content=_(NinjaError.INVALID_USERNAME),
        # content=_(NinjaError.PASSWORD_TOO_SHORT) % {"min_length": 7},
        content=_(NinjaError.PASSWORD_TOO_SHORT, min_length=7),
        # content=_("Hello World"),
    )


@app.exception_handler(LazyNinjaException)
async def lazy_ninja_exception_handler(request: Request, exc: NinjaException):
    return JSONResponse(
        status_code=418,
        content=str(_l(NinjaError.INVALID_USERNAME)),
        # content=str(_l(NinjaError.PASSWORD_TOO_SHORT)) % {"min_length": 7},
        # content=str(_l(NinjaError.PASSWORD_TOO_SHORT, min_length=7)),
        # content=str(_l("Hello World")),
    )


@app.get("/")
async def index():
    raise NinjaException


@app.get("/lazy")
async def lazy_index():
    raise LazyNinjaException


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
