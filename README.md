# Website Analytics Backend (Ingestion + Processor + Reporting)

This project implements a high-performance backend analytics system with **asynchronous event ingestion**, **background processing**, and **reporting APIs**.  
It is designed based on the assignment requirements to handle fast event intake without blocking clients.

---

# 🚀 Architecture Overview

The system is composed of **three services**:

## 1. Ingestion API (FAST)
- Endpoint: `POST /event`
- Job: validate request, **push event immediately into an async queue**, return `202 Accepted`.
- Does **NOT** wait for the database write.
- Built using **Flask**.
- Queue used: **in-memory Python queue (Queue())**.

## 2. Processor Worker (Background Worker)
- Continuously pulls events from the queue.
- Processes each event and stores it into **SQLite database (events.db)**.
- Runs as an independent service using:  
  ```bash
  python -m processor.worker
