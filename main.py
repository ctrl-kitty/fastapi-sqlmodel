import uvicorn
from fastapi import FastAPI
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, debug=settings.DEBUG)
