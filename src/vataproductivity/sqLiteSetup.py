import sqlite3

conn = sqlite3.connect('task.db')
c = conn.cursor()
c.execute("""CREATE TABLE tasks
(
    name text PRIMARY KEY,
    time integer
    )""")
#c.execute("DROP TABLE tasks")
conn.commit()
conn.close()