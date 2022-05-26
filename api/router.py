from fastapi import FastAPI
# todo оформить как роутер
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
