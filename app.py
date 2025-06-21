from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mart_db"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit_visitor', methods=['POST'])
def submit_visitor():
    try:
        gender = request.form['gender']
        age_group = request.form['age_group']
        visit_date = request.form['visit_date']
        comment = request.form.get('comment', '')

        if not all([gender, age_group, visit_date]):
            flash("All fields except comment are required!", "error")
            return redirect(url_for('form'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO visitors (gender, age_group, comment, visit_date)
            VALUES (%s, %s, %s, %s)
        ''', (gender, age_group, comment, visit_date))
        conn.commit()
        conn.close()

        flash("Visitor data recorded successfully!", "success")
        return redirect(url_for('dashboard'))

    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('form'))

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM visitors ORDER BY visit_date DESC, created_at DESC")
    visitors = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM visitors")
    total_visits = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM visitors WHERE visit_date = CURDATE()")
    today_visits = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM visitors WHERE gender = 'Male'")
    male_visits = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM visitors WHERE gender = 'Female'")
    female_visits = cursor.fetchone()[0]

    cursor.execute("SELECT gender, COUNT(*) FROM visitors GROUP BY gender")
    gender_stats = cursor.fetchall()

    cursor.execute("SELECT age_group, COUNT(*) FROM visitors GROUP BY age_group")
    age_stats = cursor.fetchall()

    cursor.execute("SELECT visit_date, COUNT(*) FROM visitors GROUP BY visit_date ORDER BY visit_date")
    date_stats = cursor.fetchall()

    conn.close()

    return render_template("dashboard.html",
                           visitors=visitors,
                           total_visits=total_visits,
                           today_visits=today_visits,
                           male_visits=male_visits,
                           female_visits=female_visits,
                           gender_stats=gender_stats,
                           age_stats=age_stats,
                           date_stats=date_stats)

if __name__ == '__main__':
    app.run(debug=True)
