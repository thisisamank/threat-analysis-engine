import fastapi as FastAPI

from engine import Engine

app = FastAPI.FastAPI()
engine = Engine()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/search/{attack_id}")
def search(attack_id: str):
    return engine.search(attack_id)
