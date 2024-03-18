from fastapi.responses import JSONResponse
from fastapi import HTTPException, status, Request
from fastapi.exceptions import RequestValidationError


class SchemaValidationError(HTTPException):
    @classmethod
    async def validation_exception_handler(cls, request: Request, exc: RequestValidationError):
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": exc.errors()},
            )

