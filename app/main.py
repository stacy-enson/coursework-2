print("MAIN.PY HAS STARTED EXECUTING")

from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents


def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    # 1. Connect to database
    conn = connect_database()
    print("Database connected")

    # 2. Create tables
    create_all_tables(conn)
    print("Tables created")

    # 3. Migrate users
    migrate_users_from_file()
    print("Users migrated")

    # 4. Register user
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)

    # 5. Login user
    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # 6. Insert incident (THIS DEFINES incident_id)
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )

    print("Incident ID:", incident_id)

    # 7. Fetch incidents
    incidents = get_all_incidents()
    print("Total incidents:", len(incidents))

    # 8. Close DB
    conn.close()
    print("Database closed")


if __name__ == "__main__":
    main()
