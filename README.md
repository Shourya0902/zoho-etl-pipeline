# Zoho CRM ETL & Sales Analytics Dashboard

## Overview
This project implements an end-to-end data pipeline to automatically extract CRM data from Zoho, transform it using Python, and load it into Google Sheets for reporting and analysis. The processed data is visualised through interactive Looker dashboards to support sales and pipeline tracking.

The system is fully automated and runs on a daily schedule, ensuring up-to-date and reliable reporting without manual intervention.

---

## Problem Statement
Sales and operations teams often rely on manual CRM exports, which can lead to:
- Delayed and outdated reports
- Inconsistent data across teams
- Limited visibility into pipeline performance

This project addresses these issues by providing a structured, automated reporting system with clear and accessible business metrics.

---

## Architecture
The data flows through the following steps:

1. Zoho CRM API is queried for Leads and Deals data  
2. Python scripts extract, clean, and transform the data  
3. Processed data is loaded into Google Sheets  
4. Looker connects to Google Sheets for reporting  
5. GitLab CI/CD schedules and executes the pipeline daily  

![Architecture Diagram](architecture.png)

---

## Key Features
- Automated ETL pipeline built using Python  
- OAuth 2.0 authentication for Zoho CRM and Google Sheets  
- Scheduled execution using GitLab CI/CD  
- Daily refreshed CRM data without manual exports  
- Interactive Looker dashboards with filters and drill-downs  

---

## Dashboard Overview
The Looker dashboard provides visibility into key sales and pipeline metrics, including:
- Daily leads created
- Daily deals created
- Deal stages and pipeline value
- Sales performance by owner
- Date and owner-level filtering for analysis

The dashboard is designed for non-technical users and focuses on decision-ready metrics.

![Uploading Screenshot 2026-02-19 at 01.17.37.png…]()


---

## Pipeline & Performance Insights
The dashboard enables users to:
- Track how deals progress across stages
- Monitor pipeline value and revenue distribution
- Compare deal volume and value across sales owners
- Identify trends and potential bottlenecks in the funnel

![Pipeline by Stage](pipeline_by_stage.png)

---

## Automation
The pipeline is executed daily using a scheduled GitLab CI/CD job:
- Authentication tokens are refreshed securely
- Data extraction, transformation, and loading run automatically
- Google Sheets is updated with the latest data
- Looker dashboards reflect updated data without manual refresh

![GitLab CI/CD Pipeline](ci_pipeline.png)

---

## Tech Stack
- **Programming Language:** Python  
- **Data Processing:** Pandas  
- **APIs:** Zoho CRM API, Google Sheets API  
- **Automation:** GitLab CI/CD  
- **Storage:** Google Sheets  
- **Visualisation:** Looker  

---
## Repository Structure

├── src/
│ ├── extract.py
│ ├── transform.py
│ └── load.py
├── .gitlab-ci.yml
├── requirements.txt
└── README.md


---

## Example Use Cases
- Sales managers tracking pipeline value and deal progress  
- Leadership monitoring individual and team performance  
- Operations teams analysing lead and deal trends  
- Business users accessing consistent daily reports  

---

## Future Improvements
- Load data into a relational database (PostgreSQL / BigQuery)
- Add data validation and quality checks
- Implement logging and alerting for pipeline failures
- Introduce conversion rate and deal velocity metrics

---

## Why This Project Matters
This project demonstrates the ability to:
- Build reliable and automated data pipelines
- Work with real-world APIs and authentication flows
- Deliver business-ready analytics and dashboards
- Own the full data lifecycle from source to reporting


## Repository Structure
