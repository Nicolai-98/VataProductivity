import sqlite3

conn = sqlite3.connect('task.db')

c = conn.cursor()

c.execute("""CREATE TABLE tasks
(
    name text PRIMARY KEY,
    time integer
    )""")
# c.execute("INSERT INTO tasks VALUES ('testName', 0)")
# c.execute("SELECT * FROM tasks WHERE name='testName'")
# print(c.fetchone())
# c.execute("DROP TABLE tasks")

conn.commit()

conn.close()