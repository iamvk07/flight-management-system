from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/flightdb")

def get_db():
    return psycopg2.connect(DB_URL)

@app.route("/api/flights", methods=["GET"])
def get_flights():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.id, f.flight_number, f.departure_time, f.arrival_time,
               f.status, r.origin, r.destination, a.tail_number
        FROM flights f
        JOIN routes r ON f.route_id = r.id
        JOIN aircraft a ON f.aircraft_id = a.id
        ORDER BY f.departure_time
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify([{
        "id": r[0], "flight_number": r[1],
        "departure": r[2].isoformat() if r[2] else None,
        "arrival": r[3].isoformat() if r[3] else None,
        "status": r[4], "origin": r[5],
        "destination": r[6], "aircraft": r[7]
    } for r in rows])

@app.route("/api/flights/<int:flight_id>", methods=["GET"])
def get_flight(flight_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM flights WHERE id = %s", (flight_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        return jsonify({"error": "Flight not found"}), 404
    return jsonify({"id": row[0], "flight_number": row[1], "status": row[5]})

@app.route("/api/flights", methods=["POST"])
def create_flight():
    data = request.json
    required = ["flight_number", "route_id", "aircraft_id", "departure_time", "arrival_time"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id FROM flights
        WHERE aircraft_id = %s AND status != 'cancelled'
        AND (departure_time, arrival_time) OVERLAPS (%s::timestamptz, %s::timestamptz)
    """, (data["aircraft_id"], data["departure_time"], data["arrival_time"]))
    conflict = cur.fetchone()
    if conflict:
        cur.close(); conn.close()
        return jsonify({"error": "Aircraft scheduling conflict", "conflict_flight_id": conflict[0]}), 409
    cur.execute("""
        INSERT INTO flights (flight_number, route_id, aircraft_id, departure_time, arrival_time)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
    """, (data["flight_number"], data["route_id"], data["aircraft_id"],
          data["departure_time"], data["arrival_time"]))
    flight_id = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return jsonify({"id": flight_id, "message": "Flight created"}), 201

@app.route("/api/flights/<int:flight_id>", methods=["PUT"])
def update_flight(flight_id):
    data = request.json
    allowed = ["status", "departure_time", "arrival_time"]
    updates = {k: v for k, v in data.items() if k in allowed}
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    conn = get_db()
    cur = conn.cursor()
    set_clause = ", ".join(f"{k} = %s" for k in updates)
    cur.execute(f"UPDATE flights SET {set_clause} WHERE id = %s",
                list(updates.values()) + [flight_id])
    conn.commit(); cur.close(); conn.close()
    return jsonify({"message": "Flight updated"})

@app.route("/api/aircraft", methods=["GET"])
def get_aircraft():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, tail_number, model, capacity, status FROM aircraft")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify([{"id": r[0], "tail_number": r[1], "model": r[2],
                     "capacity": r[3], "status": r[4]} for r in rows])

@app.route("/api/weather/<iata>", methods=["GET"])
def get_weather(iata):
    import random
    conditions = ["Clear", "Partly Cloudy", "Overcast", "Rain", "Thunderstorm", "Snow", "Fog"]
    return jsonify({
        "airport": iata.upper(),
        "condition": random.choice(conditions),
        "temp_c": round(random.uniform(-10, 35), 1),
        "wind_kmh": random.randint(0, 80),
        "visibility_km": round(random.uniform(1, 15), 1),
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
