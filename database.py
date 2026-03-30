import mysql.connector

# Database connection configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'HHH###azzing_559',
    'database': 'job_tracker'
}

def get_db_connection():
    """Create and return a new database connection"""
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")
        return None