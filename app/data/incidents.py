# app/data/incidents.py

import pandas as pd
from app.data.db import connect_database
# Insert a new incident into the cyber_incidents table

def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident record into the database.
    Returns the ID of the newly inserted incident.
    """
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cyber_incidents 
            (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))

    conn.commit()
    incident_id = cursor.lastrowid   
    conn.close()

    return incident_id
# Get all incidents as a pandas DataFrame
def get_all_incidents():
    """
    Return all cyber incidents as a pandas DataFrame.
    """
    conn = connect_database()

    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )

    conn.close()
    return df
