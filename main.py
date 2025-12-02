from app.data.db import connect_database
from app.data.schema import create_all_tables

def main():
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

if __name__ == "__main__":
    main()