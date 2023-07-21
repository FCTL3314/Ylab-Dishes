from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def index():
    return 'pong'
