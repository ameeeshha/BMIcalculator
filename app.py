
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",  # Update this if you have a password
    database="bmi_db"
)
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    bmi = None
    status = None
    name = None
    # Fetch all records from the database
    cursor.execute("SELECT * FROM bmi_records")
    past_records = cursor.fetchall()  # List of all previous records

    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])

        # Calculate BMI
        bmi = round(weight / (height * height), 2)

        # Determine BMI status
        if bmi < 18.5:
            status = "Underweight"
        elif 18.5 <= bmi < 24.9:
            status = "Normal weight"
        elif 25 <= bmi < 29.9:
            status = "Overweight"
        else:
            status = "Obese"

        # Insert the new record into the database
        cursor.execute("INSERT INTO bmi_records (name, age, height, weight, bmi, status) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, age, height, weight, bmi, status))
        conn.commit()

    # Render the template with past records and any new calculated BMI data
    return render_template('index.html', bmi=bmi, status=status, name=name, past_records=past_records)

@app.route('/delete/<int:id>', methods=['GET'])
def delete_record(id):
    # Delete the record from the database
    cursor.execute("DELETE FROM bmi_records WHERE id = %s", (id,))
    conn.commit()

    # Redirect back to the index route to refresh the page
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
