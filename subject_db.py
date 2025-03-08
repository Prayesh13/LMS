import mysql.connector

def get_subjects(semester, department):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",   # Corrected host format
            port=3306,          # Added port separately
            user="root",
            password="",  
            database="esp"
        )
        cursor = conn.cursor()

        # Base query
        query = """
        SELECT Subcode, SubjectName, Category, Semester, Youtube_Resources, Other_Resources 
        FROM subjects 
        WHERE Semester = %s
        """
        
        params = [semester]
        if department:
            query += " AND Department = %s"  # Use Department column for filtering
            params.append(department)
        
        cursor.execute(query, params)
        subjects = cursor.fetchall()

        return subjects

    except mysql.connector.Error as err:
        print("Error:", err)
        return []

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

