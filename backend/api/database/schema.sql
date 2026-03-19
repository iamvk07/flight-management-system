-- Flight Management System Database Schema
-- Vedant Kadam

CREATE TABLE aircraft (
    id           SERIAL PRIMARY KEY,
    tail_number  VARCHAR(10) UNIQUE NOT NULL,
    model        VARCHAR(60) NOT NULL,
    capacity     INT NOT NULL CHECK (capacity > 0),
    status       VARCHAR(20) NOT NULL DEFAULT 'available'
                 CHECK (status IN ('available', 'in_flight', 'maintenance', 'retired')),
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE routes (
    id             SERIAL PRIMARY KEY,
    origin         CHAR(3) NOT NULL,
    destination    CHAR(3) NOT NULL,
    distance_km    INT CHECK (distance_km > 0),
    estimated_duration_min INT,
    CHECK (origin <> destination)
);
CREATE UNIQUE INDEX uq_routes ON routes(origin, destination);

CREATE TABLE flights (
    id             SERIAL PRIMARY KEY,
    flight_number  VARCHAR(10) UNIQUE NOT NULL,
    route_id       INT NOT NULL REFERENCES routes(id) ON DELETE RESTRICT,
    aircraft_id    INT NOT NULL REFERENCES aircraft(id) ON DELETE RESTRICT,
    departure_time TIMESTAMPTZ NOT NULL,
    arrival_time   TIMESTAMPTZ NOT NULL,
    status         VARCHAR(20) NOT NULL DEFAULT 'scheduled'
                   CHECK (status IN ('scheduled', 'boarding', 'departed', 'arrived', 'delayed', 'cancelled')),
    gate           VARCHAR(6),
    created_at     TIMESTAMPTZ DEFAULT NOW(),
    CHECK (arrival_time > departure_time)
);

CREATE TABLE weather_logs (
    id           SERIAL PRIMARY KEY,
    airport_iata CHAR(3) NOT NULL,
    condition    VARCHAR(40),
    temp_c       DECIMAL(4,1),
    wind_kmh     INT,
    visibility_km DECIMAL(4,1),
    recorded_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Seed data
INSERT INTO aircraft (tail_number, model, capacity, status) VALUES
    ('C-FGDT', 'Boeing 737-800', 162, 'available'),
    ('C-GJAZ', 'Airbus A320', 150, 'available'),
    ('C-FLSF', 'Bombardier Q400', 78, 'available'),
    ('C-GKOF', 'Boeing 787-9', 296, 'maintenance');

INSERT INTO routes (origin, destination, distance_km, estimated_duration_min) VALUES
    ('YFC', 'YYZ', 1300, 110),
    ('YYZ', 'YVR', 3350, 280),
    ('YFC', 'YHZ', 270, 55),
    ('YYZ', 'YUL', 500, 80);

INSERT INTO flights (flight_number, route_id, aircraft_id, departure_time, arrival_time, gate, status) VALUES
    ('AC201', 1, 1, NOW() + INTERVAL '2 hours', NOW() + INTERVAL '3h 50m', 'A4', 'scheduled'),
    ('AC310', 2, 2, NOW() + INTERVAL '5 hours', NOW() + INTERVAL '9h 40m', 'B12', 'scheduled'),
    ('PD520', 3, 3, NOW() + INTERVAL '1 hour',  NOW() + INTERVAL '1h 55m', 'C2', 'boarding');
