from flask import Flask,request,render_template,redirect,url_for,flash,session
from werkzeug.security import check_password_hash
from datetime import datetime
import sqlite3
app=Flask(__name__)
app.secret_key="secret"
def student_db():
    return sqlite3.connect("student.db")
def staff_db():
    return sqlite3.connect("staff.db")
@app.route('/')
def home():
    return render_template("login.html")
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        role=request.form.get("role")
        mail=request.form.get("mail")
        password=request.form.get("password")

        if role=="student":
            con=student_db()
            con.row_factory=sqlite3.Row
            cur=con.cursor()
            cur.execute("""select roll,password from students where mail=?""",(mail,))
            student=cur.fetchone()
            con.close()
            if student is None:
                flash("user not found")
                return redirect(url_for("home"))
            
            if check_password_hash(student[1],password):
                session["user"]={"role":"student","id":student[0]}
                flash("welcome back!")
                return redirect(url_for("dashboard"))
            else:
                flash("wrong password")
                return redirect(url_for("home"))
            
        elif role=="staff":
            return f"staff"
        
        else:
            return f"sorry"
    return render_template("login.html")
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("login requied")
        return redirect(url_for("home"))
    roll=session["user"]["id"].upper()
    con=student_db()
    con.row_factory=sqlite3.Row 
    cur=con.cursor()
    #Total subject
    cur.execute("""SELECT COUNT(*)  FROM subjects""")
    total_subjects=cur.fetchone()[0]
    #overall Attendance 
    cur.execute("""SELECT AVG(percentage) FROM attendance WHERE roll =?""",(roll,))
    attendance=round(cur.fetchone()[0] or 0,2)
    #pending assignment
    cur.execute("SELECT COUNT(*) FROM assignments WHERE roll=? and status='pending'",(roll,))
    assignments=cur.fetchone()[0]    #schedule
    today=datetime.now().strftime("%A")
    cur.execute("SELECT time,subject,faculty FROM schedule WHERE roll=? AND day=?",(roll,today,))
    schedule=cur.fetchall()
    cur.execute("""SELECT subjects.subject_name,attendance.percentage FROM attendance
                JOIN subjects ON attendance.subject_id=subjects.id
                WHERE attendance.roll=?""",(roll,))
    subject_attendance=cur.fetchall()
    #upcoming work
    cur.execute("""
    SELECT 
        assignments.title,
        assignments.time,
        subjects.subject_name
    FROM assignments
    JOIN subjects 
    ON assignments.subject_id = subjects.id
    WHERE assignments.roll=? 
    AND assignments.status='pending'
    ORDER BY assignments.time ASC
""",(roll,))

    upcoming_assignments = cur.fetchall()
    con.close()
    return render_template("dashboard.html",total_subjects=total_subjects,attendance=attendance,
                           assignments=assignments,schedule=schedule,
                           subject_attendance=subject_attendance,
                           upcoming_assignments=upcoming_assignments
                           )
if __name__=="__main__":
    app.run(debug=True)