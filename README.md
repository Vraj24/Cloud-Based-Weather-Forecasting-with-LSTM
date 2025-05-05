# 🌦️ Cloud-Based Distributed Weather Forecasting System Using Real-Time Data

A scalable, cloud-native weather forecasting system that collects real-time data from NOAA, processes it using AWS services (Kinesis, Lambda, S3, SageMaker), and generates 7-day forecasts with alerting and visualization capabilities.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Components](#system-components)
- [Setup & Deployment](#setup--deployment)
- [Alerting Mechanism](#alerting-mechanism)
- [Dashboard Demo](#dashboard-demo)
- [Challenges & Mitigations](#challenges--mitigations)
- [License](#license)

---

## 🧠 Overview

This project aims to provide real-time and accurate weather forecasting using a distributed architecture. It uses live weather data from NOAA’s GHCND API and feeds it into an end-to-end machine learning pipeline built entirely on AWS.

Key goals:
- Automate live weather data ingestion
- Train and deploy LSTM models for 7-day forecasts
- Visualize predictions using a web dashboard
- Trigger alerts for extreme weather conditions and cost usage

---

## 🏗️ Architecture

NOAA API → Python Script → AWS Kinesis → Lambda (to S3) ↓ Lambda (Cleaner + Merger) ↓ Cleaned CSV → SageMaker (LSTM) ↓ Forecast Output → S3 → Streamlit ↓ Alerts via SNS

markdown
Copy
Edit

---

## ✅ Features

- 🌐 Real-time ingestion from NOAA using `requests`
- 🧪 JSON-to-CSV dataset cleaning using pandas in Lambda
- 🧠 LSTM-based 7-day forecast using 14-day historical data
- 📤 Data streamed via Amazon Kinesis
- 📦 Forecast stored in S3 (`forecast_7day.csv`)
- 📊 Visualized using Streamlit dashboard
- 🔔 Severe weather and AWS Budget alerts via SNS

---

## 🧰 Tech Stack

| Category          | Technology                                      |
|-------------------|--------------------------------------------------|
| Cloud Services    | AWS Lambda, Kinesis, S3, SageMaker, SNS         |
| Data Source       | NOAA GHCND API                                  |
| ML Framework      | PyTorch (LSTM Model)                            |
| Processing        | pandas, NumPy                                   |
| Visualization     | Streamlit                                       |
| Alerting          | AWS SNS                                         |
| Cost Monitoring   | AWS Budgets                                     |
| Language          | Python 3.9                                      |

---

## ⚙️ System Components

### 🔁 Data Ingestion
- A Lambda function fetches real-time NOAA data using the `GHCND:USW00023234` station (LAX).
- The script pushes structured records into **Amazon Kinesis**.

### 📦 Data Storage
- Another Lambda function reads from Kinesis and writes JSON data into **S3** (`weather_data/`).

### 🧹 Data Cleaning
- A cleaning Lambda merges JSONs and produces `cleaned_weather_dataset.csv` using pandas.

### 🤖 LSTM Forecasting
- A multivariate LSTM model trained on 14-day sequences forecasts 7 days of:
  - Wind (`AWND`, `WSF2`)
  - Temperature (`TMAX`, `TMIN`)
  - Precipitation (`PRCP`)
  - Weather conditions (`WT08`)

### 📊 Visualization
- Streamlit dashboard allows users to upload `forecast_7day.csv` and view feature-wise plots.

### ⚠️ Alerting
- A Lambda function checks the forecast for:
  - `WT08 == 1` (Storm)
  - `TMAX > 100°F` (Heat)
  - `WSF2 > 50` (High Wind)
- Alerts are sent via **SNS email notifications**.

---

## 🚀 Setup & Deployment

1. **S3 Bucket Setup**  
   Create a bucket: `kinesis-lambda-s3-bucket1`

2. **NOAA API Token**  
   [Register here](https://www.ncdc.noaa.gov/cdo-web/token)

3. **Environment Variables for Lambda**
   ```env
   NOAA_API_TOKEN = <your_token>
   AWS_REGION = us-east-1
   KINESIS_STREAM_NAME = weather-stream
Create and Connect

Amazon Kinesis Stream: weather-stream

IAM Roles for Lambda & SageMaker

Lambda Layer for pandas (optional): Klayers-p39-pandas

Train LSTM Model Save lstm_multivariate_7day.pth to S3 or local

Run Forecast Script outputs forecast_7day.csv

Launch Dashboard

bash
Copy
Edit
streamlit run streamlit_app.py
📢 Alerting Mechanism
Weather alert Lambda triggers when:

WT08 == 1 → Storm

TMAX > 100°F → High temperature

WSF2 > 50 mph → Wind alert

SNS topics send emails to subscribed addresses.

📊 Dashboard Demo
Feature	Description
Upload CSV	Accepts forecast_7day.csv
Graphs	Line charts for 11+ features
Labeling	Forecast dates + severity flags

streamlit_app.py handles dynamic charting and date filtering.

🧱 Challenges & Mitigations
Challenge	Mitigation
NOAA API rate limits	Retry logic, date fallback
Lambda size limits (pandas)	Switched to Lambda layers
Cost of SageMaker	Spot instances + local prototyping
Power BI S3 issues	Replaced with Streamlit

📄 License
This project is licensed under the MIT License. See LICENSE for more details.

📬 Contact
For questions or feedback, reach out via GitHub or email the team directly.

---

