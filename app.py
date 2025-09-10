from flask import Flask, request, render_template, redirect, url_for
import joblib
import pandas as pd
import sqlite3

app = Flask(__name__)

# Load the trained model
model = joblib.load("rf_model.pkl")
# Intialize database
def init_db():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS transactions (" 
              "Id INTEGER PRIMARY KEY AUTOINCREMENT,"
              "trans_hour INTEGER,"
              "trans_day INTEGER,"
              "trans_month INTEGER,"
              "trans_year INTEGER,"
              "trans_amount FLOAT,"
              "upi_number INTEGER,"
              "prediction TEXT)")
    conn.commit()
    conn.close()
    
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    form_data = request.form
    action = request.form['action']
    
    input_data = {
        "trans_hour": int(form_data['trans_hour']),
        "trans_day": int(form_data['trans_day']),
        "trans_month": int(form_data['trans_month']),
        "trans_year": int(form_data['trans_year']),
        "trans_amount": float(form_data['trans_amount'])
        }
    upi_number = int(form_data['upi_number'])  # Add UPI number

    # Create a DataFrame from input
    df = pd.DataFrame([input_data])
    
    print("Model ko diya gaya input DataFrame:")
    print(df)
    print(df.dtypes)

    # Predict with the model
    prediction = model.predict(df)[0]
    # Convert prediction to label
    result = "Fraud" if prediction == 1 else "Not Fraud"
    
    if action == 'submit':
        # Save to database
        conn = sqlite3.connect('transactions.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO transactions (trans_hour, trans_day, trans_month, "
            "trans_year, trans_amount, upi_number, prediction) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (input_data["trans_hour"], input_data["trans_day"],
                input_data["trans_month"],
                input_data["trans_year"], input_data["trans_amount"],
                upi_number, result))
        conn.commit()
        conn.close()
        
    return render_template('index.html', result=result)
@app.route('/history')
def history():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    records = c.fetchall()
    conn.close()
    return render_template('history.html', records=records)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('history'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    if request.method == 'POST':
        form_data = request.form
        c.execute(
            "UPDATE transactions SET trans_hour=?, trans_day=?, trans_month=?,"
            "trans_year=?, "
            "trans_amount=?, upi_number=? WHERE id=?",
            (form_data['trans_hour'], form_data['trans_day'],
             form_data['trans_month'], form_data['trans_year'],
             form_data['trans_amount'], form_data['upi_number'], id))
        conn.commit()
        conn.close()
        return redirect(url_for('history'))
    else:
        c.execute('SELECT * FROM transactions WHERE id=?', (id,))
        record = c.fetchone()
        conn.close()
        return render_template('edit.html', record=record)


if __name__ == '__main__':
    app.run(debug=True)
