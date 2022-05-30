import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
from core.config import settings
from api.router import router
from api.exceptions import UserWithThatEmailExistException
from schema.response import ErrorResponse

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router)


@app.exception_handler(UserWithThatEmailExistException)
async def user_with_that_email_exist_exception_handler(req: Request, exc: UserWithThatEmailExistException):
    data = ErrorResponse(exc, req)
    return JSONResponse(data.__dict__)


if __name__ == '__main__':
    uvicorn.run(app, host=str(settings.BACKEND_HOST), port=settings.BACKEND_PORT, debug=settings.DEBUG)
