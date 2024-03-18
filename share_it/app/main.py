from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

import uvicorn

from share_it.app.core.config import settings
from share_it.app.user.UserController import router as user_router
from share_it.app.item.ItemController import router as item_router
from share_it.app.expection.ValidationError import SchemaValidationError


app = FastAPI(title=settings.app_title, description=settings.description)

app.include_router(user_router)
app.include_router(item_router)

app.add_exception_handler(RequestValidationError, SchemaValidationError.validation_exception_handler)


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080, reload=True)

