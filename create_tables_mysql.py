import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="root", password="Latinboyjay1", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
        CREATE TABLE temperature
        (id INT NOT NULL AUTO_INCREMENT, 
            user_id VARCHAR(250) NOT NULL,
            device_id VARCHAR(250) NOT NULL,
            high INTEGER NOT NULL,
            low INTEGER NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            date_created DATETIME NOT NULL,
            CONSTRAINT temperature_pk PRIMARY KEY (id))
        ''')

db_cursor.execute('''
        CREATE TABLE humidity
          (id INT NOT NULL AUTO_INCREMENT, 
           user_id VARCHAR(250) NOT NULL,
           device_id VARCHAR(250) NOT NULL,
           humidity INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created DATETIME NOT NULL,
           CONSTRAINT humidity_pk PRIMARY KEY (id))
        ''')

db_conn.commit()
db_conn.close()