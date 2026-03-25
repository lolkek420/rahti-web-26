from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
    return { "msg": "Hello, Dainis!" }

@app.get("/api/ip")
async def get_ip(request: Request):
    client_host = request.client.host
    return {"ip": client_host}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"id": item_id, "q": q}