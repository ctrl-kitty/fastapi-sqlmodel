import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.config import settings
from api.router import router
from api.exceptions import BaseAPIException
from schema.response import ErrorResponse

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router)


@app.exception_handler(BaseAPIException)
async def user_with_that_email_exist_exception_handler(req: Request, exc: BaseAPIException):
    data = ErrorResponse(exc, req)
    return JSONResponse(data.__dict__, status_code=data.status_code)


if __name__ == '__main__':
    uvicorn.run(app, host=str(settings.BACKEND_HOST), log_level='debug' if settings.DEBUG else "critical",
                port=settings.BACKEND_PORT, debug=settings.DEBUG)
