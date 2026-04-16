from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
from db import get_conn, create_schema

app = FastAPI()

create_schema()

class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date
    info: str

@app.get("/")
def home():
    return {"msg": "Hotel API is running!"}

@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM rooms")
        return cur.fetchall()

@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO bookings (room_id, guest_id, datefrom, dateto, info)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, room_id;
        """, [booking.room_id, booking.guest_id, booking.datefrom, booking.dateto, booking.info])
        
        result = cur.fetchone()
        return {"msg": "Booking created!", "details": result}