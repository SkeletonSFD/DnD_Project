from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI()

@app.get("/", summary="Главная ручка",tags=["основные ручки"])
def root():
    return "HELLO WORLD"

if __name__ == "__main__":
    uvicorn.run(app)