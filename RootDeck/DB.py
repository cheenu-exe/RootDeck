import sqlite3
def student():
    con=sqlite3.connect("student.db")
    cur=con.cursor()
    ##student table
    cur.execute("""CREATE TABLE IF NOT EXISTS students (
                roll TEXT NOT NULL PRIMARY KEY,
                name TEXT NOT NULL,
                mail TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
                )
                """)
    #subject
    cur.execute("""
                CREATE TABLE IF NOT EXISTS subjects(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_name TEXT
                )
                """)
    #Attendance
    cur.execute("""
                CREATE TABLE IF NOT EXISTS attendance(
                roll TEXT,
                subject_id INTEGER,
                percentage INTEGER 
                )
                """)
    #SCHEDULE
    cur.execute("""
CREATE TABLE IF NOT EXISTS schedule(
    roll TEXT,
    day TEXT,
    time TEXT,
    subject TEXT,
    faculty TEXT
)
""")
    cur.execute("""CREATE TABLE IF NOT EXISTS assignments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll TEXT NOT NULL,
    subject_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    time TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
)""")
    con.commit()
    con.close()

student()
def staff():
    con=sqlite3.connect("staff.db")
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS staffs(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                mail TEXT unique NOT NULL,
                password TEXT NOT NULL
                )"""
            )
    con.commit()
    con.close()
staff()
