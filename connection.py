import mysql.connector

def getConnection():
    try:
        con=mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="amit",
            database="invest"
        )
        return con
    except mysql.connector.Error as e:
        print(f"❌ Database Connection Error: {e}")
        


    