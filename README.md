# Travel Supplier Integration Prototype

## Author
**Mayank Gupta**

## Overview

This project is a Travel Supplier Integration Prototype built using **FastAPI**, **Temporal**, **SQLite**, and **Docker**.

The system integrates multiple hotel suppliers behind a single standardized API. It normalizes supplier responses, performs unified hotel search, manages bookings using Temporal workflows, and stores booking data in SQLite.

---

# Technology Stack

- Python 3.13
- FastAPI
- Temporal Python SDK
- SQLite
- Docker & Docker Compose
- Pydantic

---

# Features

## Supplier Integration

Implemented two hotel suppliers:

- Atlas Hotels
- Nova Stays

Each supplier supports:

- Hotel Search
- Price Retrieval
- Booking Creation
- Booking Status
- Booking Cancellation

Supplier-specific responses are converted into a common internal schema.

---

## Unified Search API

Endpoint:

```
POST /search/hotels
```

Features:

- Concurrent supplier search
- Response normalization
- Duplicate filtering
- Unified response
- Ranking based on price and availability
- Partial results if one supplier fails

---

## Booking Workflow (Temporal)

Workflow Steps

1. Receive booking request
2. Revalidate selected offer
3. Create supplier reservation
4. Save booking
5. Wait for supplier confirmation
6. Mark booking as CONFIRMED

Temporal Activities are used for:

- Booking validation
- Supplier reservation
- Database operations

---

## API Endpoints

### Search Hotels

```
POST /search/hotels
```

### Create Booking

```
POST /booking
```

### Booking Details

```
GET /booking/{booking_id}
```

### Workflow Status

```
GET /workflow/{workflow_id}
```

### Cancel Booking

```
POST /cancel/{booking_id}
```

---

# Project Structure

```
app/
│
├── activities/
├── adapters/
├── api/
├── database/
├── models/
├── services/
├── suppliers/
├── utils/
├── workflows/
└── main.py
```

---

# Database

SQLite is used to store:

- Booking Records
- Workflow IDs
- Booking Status
- Supplier References

Database file:

```
travel.db
```

---

# Running the Project

## Clone Repository

```bash
git clone https://github.com/Mayank08gupta/travel-supplier-integration.git
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start Docker

```bash
docker compose up -d
```

## Start FastAPI

```bash
uvicorn app.main:app --reload
```

## Start Temporal Worker

```bash
python -m app.workflows.worker
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

Temporal UI

```
http://localhost:8233
```

---

# Testing

Tests are available inside:

```
tests/
```

Run tests using:

```bash
pytest
```

---

# Engineering Decisions

- Adapter Pattern used for supplier integration
- Temporal used for reliable booking workflow
- FastAPI provides REST APIs
- SQLite used for lightweight persistence
- Docker used for Temporal services
- Unified schema used across suppliers

---

# Assumptions

- Supplier APIs are mocked locally.
- Authentication is not implemented.
- SQLite is sufficient for prototype purposes.
- Prices are simulated.

---

# Known Limitations

- Mock supplier APIs only
- No authentication
- Basic ranking algorithm
- Limited cancellation workflow
- Prototype implementation

---

# AI Tools Used

The following AI tools were used to accelerate development:

- ChatGPT
- AI coding assistance for debugging and documentation

The project logic, integration, testing, and validation were completed manually.

---

# Repository

https://github.com/Mayank08gupta/travel-supplier-integration
