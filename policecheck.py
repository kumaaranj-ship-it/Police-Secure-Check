# ==========================================
# SecureCheck - Professional Police Dashboard
# ==========================================

# ------------------------------------------
# Import Required Libraries
# ------------------------------------------

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

from datetime import datetime
from pathlib import Path


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DB_FILE = BASE_DIR / "securecheck.db"


# ==========================================
# DATABASE EXISTENCE CHECK
# ==========================================

if not DB_FILE.exists():

    st.error(
        f"Database file not found:\n{DB_FILE}"
    )

    st.stop()


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SecureCheck",
    layout="wide"
)


# ==========================================
# DASHBOARD TITLE
# ==========================================

st.title("SecureCheck - Police Stop Digital Ledger")

st.markdown("""
Real-time police monitoring system""")

st.markdown("---")


# ==========================================
# SQLITE CONNECTION
# ==========================================

@st.cache_resource
def get_connection():

    return sqlite3.connect(
        DB_FILE,
        check_same_thread=False
    )


conn = get_connection()


# ==========================================
# LOAD DATA FROM DATABASE
# ==========================================

@st.cache_data
def load_data():

    query = """
        SELECT
            stop_date,
            stop_time,
            country_name,
            driver_gender,
            driver_age,
            driver_race,
            violation,
            search_conducted,
            search_type,
            stop_outcome,
            is_arrested,
            stop_duration,
            drugs_related_stop,
            vehicle_number
        FROM traffic_stops
    """

    df = pd.read_sql_query(query, conn)


    # --------------------------------------
    # Empty Dataset Check
    # --------------------------------------

    if df.empty:

        return df


    # --------------------------------------
    # Convert Date Column
    # --------------------------------------

    df["stop_date"] = pd.to_datetime(
        df["stop_date"],
        errors="coerce"
    ).dt.date


    # --------------------------------------
    # Clean Time Column
    # --------------------------------------

    df["stop_time"] = (
        df["stop_time"]
        .astype(str)
        .str.split(".")
        .str[0]
    )


    # --------------------------------------
    # Standardize Gender Values
    # --------------------------------------

    df["driver_gender"] = (
        df["driver_gender"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df.loc[
        df["driver_gender"].isin(["male", "m"]),
        "driver_gender"
    ] = "M"

    df.loc[
        df["driver_gender"].isin(["female", "f"]),
        "driver_gender"
    ] = "F"


    # --------------------------------------
    # Keep Valid Genders Only
    # --------------------------------------

    df = df[
        df["driver_gender"].isin(["M", "F"])
    ]


    # --------------------------------------
    # Clean Vehicle Numbers
    # --------------------------------------

    df["vehicle_number"] = (
        df["vehicle_number"]
        .astype(str)
        .str.strip()
        .str.upper()
    )


    # --------------------------------------
    # Remove Important Missing Values
    # --------------------------------------

    df = df.dropna(
        subset=[
            "stop_date",
            "stop_time",
            "vehicle_number",
            "violation",
            "driver_age",
            "stop_duration"
        ]
    )


    return df


df = load_data()


# ==========================================
# EMPTY DATA CHECK
# ==========================================

if df.empty:

    st.error("No data found in database.")

    st.stop()


# ==========================================
# SIDEBAR MENU
# ==========================================

st.sidebar.title("Dashboard Menu")


menu = st.sidebar.radio(

    "Select Section",

    [
        "Operations Dashboard",
        "Analytics Dashboard"
    ]
)


# ==========================================
# OPERATIONS DASHBOARD
# ==========================================

if menu == "Operations Dashboard":


    # ======================================
    # FILTER RECORDS
    # ======================================

    st.header("Filter Records")


    country_filter = st.selectbox(

        "Select Country",

        ["All"] +

        sorted(
            df["country_name"]
            .dropna()
            .unique()
            .tolist()
        )
    )


    gender_filter = st.selectbox(
        "Select Gender",
        ["All", "M", "F"]
    )


    violation_filter = st.selectbox(

        "Select Violation",

        ["All"] +

        sorted(
            df["violation"]
            .dropna()
            .unique()
            .tolist()
        )
    )


    # ======================================
    # APPLY FILTERS
    # ======================================

    filtered_df = df.copy()


    if country_filter != "All":

        filtered_df = filtered_df[
            filtered_df["country_name"]
            ==
            country_filter
        ]


    if gender_filter != "All":

        filtered_df = filtered_df[
            filtered_df["driver_gender"]
            ==
            gender_filter
        ]


    if violation_filter != "All":

        filtered_df = filtered_df[
            filtered_df["violation"]
            ==
            violation_filter
        ]


    # ======================================
    # KPI METRICS
    # ======================================

    total_stops = len(filtered_df)

    total_arrests = (
        filtered_df["is_arrested"]
        .sum()
    )

    drug_related_stops = (
        filtered_df["drugs_related_stop"]
        .sum()
    )

    searches_conducted = (
        filtered_df["search_conducted"]
        .sum()
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Stops",
        total_stops
    )

    col2.metric(
        "Total Arrests",
        int(total_arrests)
    )

    col3.metric(
        "Drug Related Stops",
        int(drug_related_stops)
    )

    col4.metric(
        "Searches Conducted",
        int(searches_conducted)
    )


    st.markdown("---")


    # ======================================
    # TRAFFIC SOURCE DATA
    # ======================================

    st.header("Traffic Stops Source Data")


    st.dataframe(

        filtered_df.sort_values(

            ["stop_date", "stop_time"],

            ascending=False
        ),

        use_container_width=True
    )


    st.markdown("---")


    # ======================================
    # VEHICLE INTELLIGENCE SEARCH
    # ======================================

    st.header("Vehicle Intelligence Search")

    st.markdown("""
    Search police stop records using
    vehicle number to generate
    automated incident summaries.
    """)


    # --------------------------------------
    # Vehicle Search Form
    # --------------------------------------

    with st.form("vehicle_search_form"):

        vehicle_input = st.text_input(
            "Enter Vehicle Number or Last 4 Digits"
        )

        generate_report = st.form_submit_button(
            "Generate Vehicle Report"
        )


    # ======================================
    # GENERATE VEHICLE REPORT
    # ======================================

    if generate_report:


        if vehicle_input.strip() == "":

            st.warning(
                "Please enter a vehicle number."
            )


        else:

            # ----------------------------------
            # GLOBAL SEARCH
            # ----------------------------------

            matches = df[

                df["vehicle_number"]

                .astype(str)

                .str.strip()

                .str.upper()

                .str.contains(
                    vehicle_input.upper()
                )
            ]


            # ----------------------------------
            # NO RECORDS
            # ----------------------------------

            if matches.empty:

                st.warning(
                    "No matching vehicle records found."
                )


            # ----------------------------------
            # GENERATE REPORTS
            # ----------------------------------

            else:

                st.success(
                    f"Records Found: {len(matches)}"
                )


                for _, r in matches.iterrows():

                    # --------------------------
                    # Format Time
                    # --------------------------

                    try:

                        formatted_time = datetime.strptime(

                            r["stop_time"],

                            "%H:%M:%S"

                        ).strftime("%I:%M %p")


                    except ValueError:

                        formatted_time = r["stop_time"]


                    # --------------------------
                    # Gender Text
                    # --------------------------

                    gender_text = (

                        "male"

                        if r["driver_gender"] == "M"

                        else "female"
                    )


                    # --------------------------
                    # Search Text
                    # --------------------------

                    if r["search_conducted"] == 1:

                        if pd.notna(r["search_type"]):

                            search_text = (
                                f"A {r['search_type']} "
                                f"was conducted."
                            )

                        else:

                            search_text = (
                                "A vehicle search "
                                "was conducted."
                            )

                    else:

                        search_text = (
                            "No search was conducted."
                        )


                    # --------------------------
                    # Arrest Text
                    # --------------------------

                    if r["is_arrested"] == 1:

                        outcome_text = (
                            "The driver was arrested."
                        )

                    else:

                        outcome_text = (
                            f"The driver received "
                            f"{r['stop_outcome']}."
                        )


                    # --------------------------
                    # Drug Text
                    # --------------------------

                    if r["drugs_related_stop"] == 1:

                        drug_text = (
                            "The stop was drug-related."
                        )

                    else:

                        drug_text = (
                            "The stop was not drug-related."
                        )


                    # --------------------------
                    # Final Report
                    # --------------------------

                    st.info(

                        f"""
Vehicle Number:
{r['vehicle_number']}

A {int(r['driver_age'])}-year-old
{gender_text} driver
was stopped for
{r['violation']}
at {formatted_time}
on {r['stop_date']}.

{search_text}

{outcome_text}

The stop lasted
{r['stop_duration']}.

{drug_text}
"""
                    )


# ==========================================
# ANALYTICS DASHBOARD
# ==========================================

elif menu == "Analytics Dashboard":


    st.header("Advanced Insights and Analytics")


    category = st.selectbox(

        "Select Analysis Category",

        [
            "Vehicle and Searches",
            "Driver Demographics",
            "Time-Based Analysis",
            "Violations Analysis",
            "Country-Level Insights",
            "Complex Analysis"
        ]
    )


    sub_options = {

        "Vehicle and Searches": [

            "Top 10 Vehicles in Drug Related Stops",

            "Most Frequently Searched Vehicles"
        ],


        "Driver Demographics": [

            "Driver Age Group with Highest Arrest Rate",

            "Gender Distribution by Country",

            "Race and Gender with Highest Search Rate"
        ],


        "Time-Based Analysis": [

            "Time of Day with Most Traffic Stops",

            "Night vs Day Arrest Likelihood"
        ],


        "Violations Analysis": [

            "Average Stop Duration by Violation",

            "Violations with Highest Search or Arrest"
        ],


        "Country-Level Insights": [

            "Countries with Highest Drug Related Stops",

            "Arrest Rate by Country and Violation"
        ],


        "Complex Analysis": [

            "Top 5 Violations with Highest Arrest Rates"
        ]
    }


    question = st.selectbox(
        "Select Question",
        sub_options[category]
    )


    # ======================================
    # RUN ANALYSIS
    # ======================================

    if st.button("Run Analysis"):

        queries = {

            "Top 10 Vehicles in Drug Related Stops": """

                SELECT
                    vehicle_number,
                    COUNT(*) AS count

                FROM traffic_stops

                WHERE drugs_related_stop = 1

                GROUP BY vehicle_number

                ORDER BY count DESC

                LIMIT 10
            """,


            "Most Frequently Searched Vehicles": """

                SELECT
                    vehicle_number,
                    COUNT(*) AS count

                FROM traffic_stops

                WHERE search_conducted = 1

                GROUP BY vehicle_number

                ORDER BY count DESC

                LIMIT 20
            """,


            "Driver Age Group with Highest Arrest Rate": """

                SELECT
                    driver_age,

                    ROUND(
                        AVG(is_arrested) * 100,
                        2
                    ) AS arrest_rate

                FROM traffic_stops

                GROUP BY driver_age

                ORDER BY arrest_rate DESC
            """,


            "Gender Distribution by Country": """

                SELECT
                    country_name,
                    driver_gender,
                    COUNT(*) AS count

                FROM traffic_stops

                GROUP BY country_name, driver_gender
            """,


            "Race and Gender with Highest Search Rate": """

                SELECT
                    driver_race,
                    driver_gender,

                    ROUND(
                        AVG(search_conducted) * 100,
                        2
                    ) AS search_rate

                FROM traffic_stops

                WHERE driver_race IS NOT NULL

                GROUP BY driver_race, driver_gender

                ORDER BY search_rate DESC
            """,


            "Time of Day with Most Traffic Stops": """

                SELECT
                    SUBSTR(stop_time,1,2) AS hour,

                    COUNT(*) AS count

                FROM traffic_stops

                GROUP BY hour

                ORDER BY count DESC
            """,


            "Night vs Day Arrest Likelihood": """

                SELECT

                    CASE

                        WHEN CAST(
                            SUBSTR(stop_time,1,2)
                            AS INT
                        )

                        BETWEEN 6 AND 17

                        THEN 'Day'

                        ELSE 'Night'

                    END AS period,

                    ROUND(
                        AVG(is_arrested) * 100,
                        2
                    ) AS arrest_rate

                FROM traffic_stops

                GROUP BY period
            """,


            "Average Stop Duration by Violation": """

                SELECT
                    violation,

                    AVG(

                        CASE

                            WHEN stop_duration='0-15 Min'
                            THEN 15

                            WHEN stop_duration='16-30 Min'
                            THEN 30

                            WHEN stop_duration='30+ Min'
                            THEN 45

                        END

                    ) AS avg_duration_minutes

                FROM traffic_stops

                GROUP BY violation
            """,


            "Violations with Highest Search or Arrest": """

                SELECT

                    violation,

                    ROUND(
                        AVG(search_conducted) * 100,
                        2
                    ) AS search_rate,

                    ROUND(
                        AVG(is_arrested) * 100,
                        2
                    ) AS arrest_rate

                FROM traffic_stops

                GROUP BY violation

                ORDER BY arrest_rate DESC
            """,


            "Countries with Highest Drug Related Stops": """

                SELECT
                    country_name,
                    COUNT(*) AS count

                FROM traffic_stops

                WHERE drugs_related_stop = 1

                GROUP BY country_name

                ORDER BY count DESC
            """,


            "Arrest Rate by Country and Violation": """

                SELECT

                    country_name,

                    violation,

                    ROUND(
                        AVG(is_arrested) * 100,
                        2
                    ) AS arrest_rate

                FROM traffic_stops

                GROUP BY country_name, violation
            """,


            "Top 5 Violations with Highest Arrest Rates": """

                SELECT

                    violation,

                    ROUND(
                        AVG(is_arrested) * 100,
                        2
                    ) AS arrest_rate

                FROM traffic_stops

                GROUP BY violation

                ORDER BY arrest_rate DESC

                LIMIT 5
            """
        }


        result_df = pd.read_sql_query(
            queries[question],
            conn
        )


        st.subheader("Query Results")


        st.dataframe(
            result_df,
            use_container_width=True
        )


        # ==================================
        # PLOTLY CHART
        # ==================================

        if len(result_df.columns) >= 2:

            fig = px.bar(

                result_df,

                x=result_df.columns[0],

                y=result_df.columns[1],

                text_auto=True,

                title=question
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )