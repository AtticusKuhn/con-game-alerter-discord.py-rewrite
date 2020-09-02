import sqlite3
conn = sqlite3.connect('data/database.db')
c = conn.cursor()
c.execute('''CREATE TABLE alertpeople
            (id text, format text)''')
c.execute("INSERT INTO alertpeople VALUES ('464954455029317633', 'FLASHPOINT')")
c.execute('''CREATE TABLE seengames
            (id text, time real)''')
c.execute("INSERT INTO seengames VALUES ('3', 12938)")
conn.commit()
conn.close()