# Corre Hoje?

Is it a good day to run outside in Porto? A small data pipeline that combines
weather (IPMA) and air quality (AQICN) data, predicts bad air days and sends a
daily alert.

## Architecture

```
Collectors (Python)  ->  MongoDB (raw)  ->  ETL  ->  PostgreSQL (clean)
                                                         |
                                     ML model  ->  FastAPI /today  ->  Telegram alert
```

## Run locally

```bash
cp .env.example .env          # set your own values
docker compose up -d          # starts MongoDB
python -m venv .venv && source .venv/bin/activate
pip install -r collectors/requirements.txt
python collectors/ipma_collector.py
```

## Roadmap

- [ ] Day 1: IPMA and AQICN collectors storing raw data in MongoDB
- [ ] Day 2: ETL (clean, merge by hour) into PostgreSQL, with tests
- [ ] Day 3: historical data and a bad-air-day model (scikit-learn)
- [ ] Day 4: FastAPI endpoint and Telegram bot
- [ ] Day 5: Kubernetes CronJobs and GitHub Actions
- [ ] Bonus: Android widget in Jetpack Compose
