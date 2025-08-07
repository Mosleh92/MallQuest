# Database Setup Guide

This guide explains how to configure the application to use PostgreSQL and run
schema migrations.

## 1. Configure Environment

Set the `DATABASE_URL` environment variable to point at your PostgreSQL
instance. The value is a standard SQLAlchemy URL, for example:

```bash
export DATABASE_URL=postgresql+psycopg2://mallquest:mallquest@localhost/mall_gamification
```

If sharding is required, also set `SHARD_COUNT` and optionally
`SHARD_STRATEGY`.

Redis is used for background tasks:

```bash
export REDIS_URL=redis://localhost:6379/0
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Run Migrations

Use Alembic to create the schema in the database. Migrations will run across all
shards if `SHARD_COUNT` is greater than one.

```bash
alembic upgrade head
```

## 4. Background Worker

The segmentation service schedules its cache refresh using an RQ job. Start a
worker to process tasks:

```bash
rq worker segmentation
```

The job reschedules itself every 24 hours.

## 5. Verification

After migrations, verify the connection by running the test suite:

```bash
pytest
```

