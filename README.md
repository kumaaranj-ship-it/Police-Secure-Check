# SecureCheck - Police Stop Digital Ledger

## Project Overview

SecureCheck is a professional police traffic stop analytics dashboard built using:

- Python
- Streamlit
- SQLite
- Pandas
- Plotly

The project simulates a real-time police monitoring and analytics system capable of:

- Managing police stop records
- Performing vehicle intelligence searches
- Generating analytics dashboards
- Running SQL-based traffic stop analysis
- Visualizing crime and enforcement patterns

---

# Project Architecture

```text
traffic_stops.xlsx
        ↓
ETL.py
(Extract → Transform → Load)
        ↓
cleaned_traffic_stops.csv
        ↓
securecheck.db
        ↓
policecheck.py
(Streamlit Dashboard)
```

---

# Folder Structure

```text
Police Secure Check/
│
├── data/
│   ├── raw/
│   │   └── traffic_stops.xlsx
│   │
│   └── processed/
│       └── cleaned_traffic_stops.csv
│
├── ETL.py
├── policecheck.py
├── securecheck.db
├── README.md
├── requirements.txt
└── SecureCheck.pptx
```

---

# Features

## Operations Dashboard

- Filter police stop records
- Country-based filtering
- Gender-based filtering
- Violation-based filtering
- KPI metrics:
  - Total Stops
  - Arrests
  - Drug-related stops
  - Searches conducted

### Vehicle Intelligence Search

Search using:
- Full vehicle number
- Partial vehicle number
- Last 4 digits

Automatically generates:
- Incident summaries
- Search details
- Arrest details
- Drug-related stop information

---

## Analytics Dashboard

### Vehicle and Searches
- Top 10 vehicles in drug-related stops
- Most frequently searched vehicles

### Driver Demographics
- Driver age group with highest arrest rate
- Gender distribution by country
- Race and gender with highest search rate

### Time-Based Analysis
- Time of day with most traffic stops
- Night vs day arrest likelihood

### Violations Analysis
- Average stop duration by violation
- Violations with highest search or arrest rate

### Country-Level Insights
- Countries with highest drug-related stops
- Arrest rate by country and violation

### Complex Analysis
- Top 5 violations with highest arrest rates

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data cleaning and transformation |
| SQLite | Database storage |
| Streamlit | Interactive dashboard |
| Plotly | Data visualization |
| OpenPyXL | Excel file handling |

---

# ETL Pipeline

The ETL pipeline is implemented in:

```text
ETL.py
```

## Extract
- Reads raw traffic stop data from Excel

File:
```text
data/raw/traffic_stops.xlsx
```

---

## Transform
Performs:
- Date conversion
- Time cleaning
- Gender standardization
- Vehicle number formatting
- Null value removal
- Duplicate removal
- Boolean conversion

---

## Load

Outputs:
- Cleaned CSV
- SQLite database

Generated files:
```text
data/processed/cleaned_traffic_stops.csv
securecheck.db
```

---

# Installation

## Clone Repository

```bash
git clone <repository_url>
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# How to Run the Project

## Step 1 — Run ETL Pipeline

```bash
python ETL.py
```

This:
- Cleans raw Excel data
- Generates processed CSV
- Creates SQLite database

---

## Step 2 — Run Streamlit Dashboard

```bash
streamlit run policecheck.py
```

---

# Database

Database used:
```text
securecheck.db
```

Main table:
```sql
traffic_stops
```

---

# Sample SQL Analysis

Example:

```sql
SELECT
    violation,
    ROUND(AVG(is_arrested) * 100, 2) AS arrest_rate
FROM traffic_stops
GROUP BY violation
ORDER BY arrest_rate DESC;
```

---

# Performance Optimization

The project uses:
- Cached database connections
- SQLite for fast querying
- Separate ETL pipeline
- Preprocessed cleaned dataset

This significantly improves dashboard loading speed.

---

# Future Improvements

- User authentication
- Real-time API integration
- Geo-mapping of incidents
- Predictive policing analytics
- Machine learning-based risk scoring
- Deployment to cloud platforms

---

# Author

Kumaaran J

---

# License

This project is for educational and portfolio purposes.
