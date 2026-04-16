import os, psycopg, time

DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/hotel_db"

def get_conn():
    for i in range(5):
        try:
            return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)
        except:
            print("База еще спит, ждем...")
            time.sleep(2)
    raise Exception("Не удалось подключиться к БД")

def create_schema():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS bookings, guests, rooms CASCADE;")
        
        cur.execute("""
            CREATE TABLE rooms (
                id SERIAL PRIMARY KEY,
                room_number INT NOT NULL,
                room_type VARCHAR DEFAULT 'Standard',
                price NUMERIC NOT NULL DEFAULT 100
            );

            CREATE TABLE guests (
                id SERIAL PRIMARY KEY,
                firstname VARCHAR NOT NULL,
                lastname VARCHAR NOT NULL
            );

            CREATE TABLE bookings (
                id SERIAL PRIMARY KEY,
                guest_id INT REFERENCES guests(id),
                room_id INT REFERENCES rooms(id),
                datefrom DATE DEFAULT now(),
                dateto DATE DEFAULT (now() + interval '1 day')
            );
            
            -- Сразу добавим одну тестовую комнату, чтобы не было пусто
            INSERT INTO rooms (room_number, room_type, price) VALUES (101, 'Lux', 500);
        """)