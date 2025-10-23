import pyodbc

def get_access_connection():
    """Create and return a connection to the Access database."""
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=c:\Users\Geeks2_PC17\Desktop\Data_Analysis\Analysis\PaymentAPI.accdb;"
    )
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to Access database: {str(e)}")
        return None

def fetch_payments():
    """Fetch payment data from Access database."""
    conn = get_access_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Payments")  # Adjust table name if different
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    except pyodbc.Error as e:
        print(f"Error fetching payments: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()