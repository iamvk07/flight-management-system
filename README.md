# Flight Management System

A full-stack flight management platform supporting flight scheduling, aircraft tracking, route management, and weather integration.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Core Logic | Java 17 |
| Data Processing | C++ (via JNI) |
| REST API | Python / Flask |
| Frontend | React 18 |
| Database | PostgreSQL 15 |
| Containerization | Docker + Docker Compose |

## Features

- ✈️ Manage flights, aircraft, routes, and schedules
- 🌤 Simulated weather data integration
- 📅 Conflict detection for overlapping flight times
- 🗄 Normalized PostgreSQL schema with full referential integrity
- 🔌 RESTful API with OpenAPI documentation
- ⚛️ React frontend for viewing and managing all data

## Project Structure

```
flight-management-system/
├── backend/
│   ├── java/
│   │   ├── FlightScheduler.java
│   │   ├── Aircraft.java
│   │   ├── Route.java
│   │   └── ValidationEngine.java
│   ├── api/
│   │   ├── app.py               # Flask app
│   │   ├── routes/
│   │   │   ├── flights.py
│   │   │   ├── aircraft.py
│   │   │   └── weather.py
│   │   └── db.py
│   └── cpp/
│       └── scheduler.cpp        # Performance-critical scheduling
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── FlightBoard.jsx
│   │   │   └── AircraftPanel.jsx
│   │   └── api/
│   │       └── client.js
├── database/
│   └── schema.sql
├── docker-compose.yml
└── README.md
```

## Quick Start

```bash
# Clone the repo
git clone https://github.com/vedantkadam07/flight-management-system
cd flight-management-system

# Start all services
docker-compose up --build

# App runs at http://localhost:3000
# API runs at http://localhost:5000
```

## Database Schema (simplified)

```sql
-- See database/schema.sql for full schema
CREATE TABLE aircraft (
  id SERIAL PRIMARY KEY,
  tail_number VARCHAR(10) UNIQUE NOT NULL,
  model VARCHAR(50),
  capacity INT,
  status VARCHAR(20) DEFAULT 'available'
);

CREATE TABLE routes (
  id SERIAL PRIMARY KEY,
  origin VARCHAR(3) NOT NULL,      -- IATA code
  destination VARCHAR(3) NOT NULL,
  distance_km INT
);

CREATE TABLE flights (
  id SERIAL PRIMARY KEY,
  flight_number VARCHAR(10) UNIQUE NOT NULL,
  route_id INT REFERENCES routes(id),
  aircraft_id INT REFERENCES aircraft(id),
  departure_time TIMESTAMPTZ,
  arrival_time TIMESTAMPTZ,
  status VARCHAR(20) DEFAULT 'scheduled'
);
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/flights | List all flights |
| POST | /api/flights | Create new flight |
| GET | /api/flights/:id | Get flight details |
| PUT | /api/flights/:id | Update flight |
| GET | /api/aircraft | List all aircraft |
| GET | /api/weather/:iata | Get weather for airport |

## Author

**Vedant Kadam** · UNB Computer Science
