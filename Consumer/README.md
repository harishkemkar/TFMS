# TFMS Consumer Module

This repository contains the **Consumer module** for the Transactional Fraud Management System (TFMS).  
It runs as an **ECS Task** triggered by new files in S3, enriches transactions using a fraud detection model, and writes results back to S3.

## Features
- S3 integration (raw → processed buckets)
- Fraud detection model (`model_rf_cal.joblib`)
- ECS task ready (Dockerfile included)
- Modular design with logging and utilities

## Directory Structure
- `consumer_runner.py` → Orchestrates file processing
- `model_integration.py` → Preprocesses records & runs ML model
- `s3_reader.py` / `s3_writer.py` → S3 I/O helpers
- `utils/` → Utility functions
- `logs/` → Logging utilities
- `requirements.txt` → Python dependencies
- `Dockerfile` → Containerization for ECS/ECR

## Usage
```bash
docker build -t tfms-consumer .
docker run -e RAW_FILE_KEY=<file_key> tfms-consumer

