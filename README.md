# Smart Log Analyzer

A small FastAPI backend for collecting and analyzing application logs.

The API can automatically classify incoming messages as `INFO`, `WARNING`,
or `ERROR`, store them in SQLite, filter log history, and expose simple
analytics.

## Features

- REST API built with FastAPI
- Automatic log-level detection
- SQLite persistence with SQLAlchemy
- Filtering by level and source
- Basic log statistics and common-message analysis
- Swagger/OpenAPI documentation
- Docker support
- Pytest API tests

## Project structure

```text
app/
├── routes/
│   └── logs.py
├── database.py
├── main.py
├── models.py
├── schemas.py
└── services.py
tests/
└── test_api.py
```

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Example

Create a log:

```bash
curl -X POST "http://127.0.0.1:8000/logs" \
  -H "Content-Type: application/json" \
  -d '{"message":"Database connection failed","source":"backend"}'
```

The service detects the message as an error:

```json
{
  "id": 1,
  "message": "Database connection failed",
  "level": "ERROR",
  "source": "backend",
  "created_at": "2026-09-19T16:00:00"
}
```

Get only errors:

```bash
curl "http://127.0.0.1:8000/logs?level=ERROR"
```

Get analytics:

```bash
curl "http://127.0.0.1:8000/stats"
```

## Run tests

```bash
pytest
```

## Docker

```bash
docker compose up --build
```

The API will be available on port `8000`.

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| POST | `/logs` | Create a log |
| GET | `/logs` | List/filter logs |
| GET | `/stats` | Log analytics |

## Possible improvements

- PostgreSQL support
- Authentication
- Date-range filtering
- Structured JSON logs
- Background ingestion
- LLM-based incident summaries
- Grafana/Prometheus integration
