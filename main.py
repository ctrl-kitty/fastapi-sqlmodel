from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.config import settings
from api.router import router
from api.exceptions import BaseAPIException
from schema.response import ErrorResponse
import os
import uvicorn
from multiprocessing import cpu_count

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router)


@app.exception_handler(BaseAPIException)
async def user_with_that_email_exist_exception_handler(req: Request, exc: BaseAPIException):
    data = ErrorResponse(exc, req)
    return JSONResponse(data.__dict__, status_code=data.status_code)


if __name__ == '__main__':
    if settings.DEBUG is True:
        uvicorn.run(app, host=str(settings.BACKEND_HOST), log_level='debug',
                    port=settings.BACKEND_PORT, debug=True)
    else:
        os.system(f'gunicorn main:app \
         --bind 0.0.0.0:{settings.BACKEND_PORT} \
         --workers {cpu_count()*settings.WORKERS_PER_THREAD} \
         -k uvicorn.workers.UvicornWorker')
