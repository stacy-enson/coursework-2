from app.data.db import connect_database
#Users table
def create_users_table(conn):
    """Create the users table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
#Cyber Incidents Table
def create_cyber_incidents_table(conn):
    """Create the cyber_incidents table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT,
            reported_by TEXT
        )
    """)
    conn.commit()
#Datasets Metadata Table
def create_datasets_metadata_table(conn):
    """Create the datasets_metadata table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            source TEXT,
            created_on TEXT
        )
    """)
    conn.commit()
#IT Tickets Table
def create_it_tickets_table(conn):
    """Create the it_tickets table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_title TEXT NOT NULL,
            ticket_description TEXT,
            priority TEXT,
            status TEXT,
            created_by TEXT,
            created_on TEXT
        )
    """)
    conn.commit()
#Creating all tables
def create_all_tables(conn):
    """Create all tables in the database."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)