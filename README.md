# SecureCheck: A Python-SQL Digital Ledger for Police Post Logs

## Project Overview

SecureCheck is a real-time police monitoring and digital ledger system developed using Python, SQLite, SQL, Pandas, and Streamlit.

The project simulates a modern police check-post management system where vehicle stop records are digitally stored, analyzed, filtered, and monitored using SQL-powered analytics and an interactive Streamlit dashboard.

The system helps law enforcement agencies:

- Track vehicle movements
- Monitor violations and arrests
- Identify suspicious activities
- Analyze traffic stop trends
- Generate automated police incident summaries
- Improve operational efficiency using SQL analytics

---

# Domain

Law Enforcement & Public Safety

---

# Skills Used

- Python
- SQL
- SQLite
- Pandas
- Streamlit
- Data Cleaning
- Data Analysis
- Data Visualization
- Dashboard Development

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and backend logic |
| SQLite | Database management |
| SQL | Querying and analytics |
| Pandas | Data cleaning and manipulation |
| Streamlit | Interactive dashboard |
| Plotly | Data visualization |

---

# Problem Statement

Police check posts often rely on manual logging systems and disconnected databases, making vehicle tracking and criminal analysis inefficient.

SecureCheck solves this problem by creating:

- A centralized SQL-based digital ledger
- Real-time vehicle intelligence search
- Automated police reporting system
- SQL-powered analytical dashboard
- Data-driven law enforcement insights

---

# Business Use Cases

- Real-time logging of vehicle stops
- Automated suspect vehicle lookup
- Crime pattern analysis
- Officer reporting dashboard
- Arrest and violation monitoring
- Traffic stop analytics
- Drug-related stop tracking
- Search and seizure analysis

---

# Dataset Features

| Column Name | Description |
|---|---|
| stop_date | Date of stop |
| stop_time | Time of stop |
| country_name | Country of stop |
| driver_gender | Gender of driver |
| driver_age | Driver age |
| driver_race | Driver race |
| violation | Type of violation |
| search_conducted | Whether search was conducted |
| search_type | Type of search |
| stop_outcome | Stop outcome |
| is_arrested | Arrest status |
| stop_duration | Duration of stop |
| drugs_related_stop | Drug-related stop status |
| vehicle_number | Vehicle identification number |

---

# Project Workflow

## Step 1: Data Cleaning

The raw Excel dataset is cleaned using Pandas.

### Cleaning Tasks Performed

- Removed columns containing all missing values
- Handled missing values
- Standardized gender values
- Cleaned vehicle numbers
- Converted dates and times
- Removed invalid records

---

## Step 2: Database Creation

The cleaned dataset is loaded into SQLite.

### Database Table

```sql
traffic_stops
```

The table stores all police stop records used by the dashboard and analytics engine.

---

## Step 3: Streamlit Dashboard

The interactive dashboard contains:

### Operations Dashboard

- Filter police records
- Dynamic KPI metrics
- Vehicle intelligence search
- Automated incident summaries
- Source traffic stop records

### Analytics Dashboard

- SQL-powered analysis
- Violation trends
- Arrest analysis
- Demographic insights
- Time-based stop analysis
- Drug-related stop reports

---

# Dashboard Features

## 1. Filter Records

Users can filter records by:

- Country
- Gender
- Violation

The filters dynamically update:

- KPI metrics
- Traffic stop source data

---

## 2. KPI Metrics

The dashboard displays:

- Total Stops
- Total Arrests
- Drug Related Stops
- Searches Conducted

---

## 3. Vehicle Intelligence Search

Users can search by:

- Full vehicle number
- Last 4 digits

The system generates automated police-style narrative summaries.

### Example Output

```text
Vehicle Number:
TN45AB1234

A 27-year-old male driver
was stopped for Speeding
at 02:30 PM
on 2020-05-12.

No search was conducted.

The driver received Citation.

The stop lasted 6-15 Min.

The stop was not drug-related.
```

---

# SQL Analysis Implemented

## Vehicle-Based Analysis

- Top vehicles involved in drug-related stops
- Most frequently searched vehicles

## Demographic Analysis

- Highest arrest rates by age
- Gender distribution by country
- Race and gender search analysis

## Time-Based Analysis

- Peak traffic stop hours
- Day vs night arrest comparison

## Violation Analysis

- Violations with highest arrests
- Search rate by violation
- Average stop duration

## Country-Level Analysis

- Drug-related stops by country
- Arrest rate by country and violation

## Complex SQL Analysis

- Top 5 violations with highest arrest rates

---

# Project Structure

```text
police check/
│
├── data/
│   ├── raw/
│   │   └── traffic_stops.xlsx
│   │
│   └── cleaned/
│       └── cleaned_traffic_stops.csv
│
├── scripts/
│   ├── data_cleaning.py
│   ├── db_connection.py
│   ├── load_to_sql.py
│   └── sql_analysis.py
│
├── app.py
├── securecheck.db
├── requirements.txt
└── README.md
```

---

# Installation

## Clone the Repository

```bash
git clone <repository-url>
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Data Cleaning

```bash
python scripts/data_cleaning.py
```

---

# Load Data into SQLite

```bash
python scripts/load_to_sql.py
```

---

# Run Streamlit Dashboard

```bash
streamlit run app.py
```

---

# Key Learnings

- Real-world data cleaning
- SQL database integration
- Streamlit dashboard development
- Dynamic filtering
- SQL analytics
- Police intelligence workflows
- Interactive data visualization
- Narrative report generation

---

# Future Enhancements

- Role-based officer login system
- Real-time vehicle blacklist alerts
- GPS-enabled tracking
- Predictive crime analysis
- Machine learning-based suspect prediction
- Multi-check-post synchronization
- Cloud database integration

---

# Project Outcomes

- Faster police record management
- Improved stop analysis
- Automated intelligence reporting
- Efficient SQL querying
- Better operational visibility
- Data-driven law enforcement decisions

---

# Author

Kumaaran J

---

# License

This project is developed for educational and portfolio purposes.