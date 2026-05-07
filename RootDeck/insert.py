import sqlite3
import random
from datetime import datetime, timedelta

con = sqlite3.connect("student.db")
cur = con.cursor()

# ---------------- SUBJECTS ---------------- #

subjects = [
    "Linear Algebra",
    "Fundamentals of Economics",
    "R Programming",
    "Principles of Electronics",
    "Data Structures",
    "Python Lab"
]

# insert subjects only if empty
cur.execute("SELECT COUNT(*) FROM subjects")

if cur.fetchone()[0] == 0:

    cur.executemany(
        "INSERT INTO subjects(subject_name) VALUES(?)",
        [(s,) for s in subjects]
    )

# ---------------- FETCH STUDENTS ---------------- #

cur.execute("SELECT roll FROM students")
students = cur.fetchall()

# ---------------- ATTENDANCE ---------------- #

cur.execute("DELETE FROM attendance")

for student in students:

    roll = student[0].upper()

    for subject_id in range(1, 7):

        percentage = random.randint(65, 98)

        cur.execute("""
            INSERT INTO attendance(roll,subject_id,percentage)
            VALUES(?,?,?)
        """, (roll, subject_id, percentage))

# ---------------- SCHEDULE ---------------- #

cur.execute("DELETE FROM schedule")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

time_slots = [
    "8:45-9:30",
    "9:30-10:15",
    "10:30-11:15",
    "11:15-12:00"
]

faculty = [
    "Dr.V.Nirmala",
    "Ms.V.Savithri",
    "Mr.R.Jeyapandiradap",
    "Dr.Sarikeha",
    "Ms.Benilin Leeba"
]

for student in students:

    roll = student[0].upper()

    for day in days:

        for i in range(4):

            cur.execute("""
                INSERT INTO schedule(
                    roll,
                    day,
                    time,
                    subject,
                    faculty
                )
                VALUES(?,?,?,?,?)
            """, (
                roll,
                day,
                time_slots[i],
                random.choice(subjects),
                random.choice(faculty)
            ))

# ---------------- ASSIGNMENTS ---------------- #

cur.execute("DELETE FROM assignments")

assignment_titles = [
    "Assignment 1",
    "Record Submission",
    "Mini Project",
    "Lab Observation",
    "Internal Preparation"
]

for student in students:

    roll = student[0].upper()

    for _ in range(4):

        subject_id = random.randint(1, 6)

        due_date = (
            datetime.now() +
            timedelta(days=random.randint(1, 15))
        ).strftime("%Y-%m-%d")

        cur.execute("""
            INSERT INTO assignments(
                roll,
                subject_id,
                title,
                time,
                status
            )
            VALUES(?,?,?,?,?)
        """, (
            roll,
            subject_id,
            random.choice(assignment_titles),
            due_date,
            "pending"
        ))

# ---------------- SAVE ---------------- #

con.commit()
con.close()

print("Fake data inserted successfully")