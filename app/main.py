from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройки CORS (как в твоем примере)
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms = [
    {"room_number": 101, "type": "Single", "price": 50, "is_booked": False},
    {"room_number": 102, "type": "Double", "price": 80, "is_booked": True},
    {"room_number": 201, "type": "Suite", "price": 150, "is_booked": False}
]


@app.get("/api/ip")
def api_ip(request: Request): 
    return { "ip": request.client.host }

@app.get("/rooms")
def get_rooms():
    return rooms