import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="root", password="Latinboyjay1", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
        DROP TABLE temperature, humidity
        ''')

db_conn.commit()
db_conn.close()