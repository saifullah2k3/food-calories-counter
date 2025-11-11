# Example: Adding a food item
def add_food_item(user_id, food_id, quantity, unit):
    # Retrieve nutritional info
    food_info = get_food_info(food_id)
    # Calculate nutritional intake based on quantity
    intake = calculate_nutrition(food_info, quantity, unit)
    # Save to user’s daily log
    save_to_log(user_id, intake)

def calculate_daily_intake(user_id, date):
    daily_log = get_user_log(user_id, date)
    totals = {}
    for item in daily_log:
        for nutrient, value in item['nutrition'].items():
            totals[nutrient] = totals.get(nutrient, 0) + value
    return totals

def assess_nutrition(totals, rda):
    feedback = {}
    for nutrient, total in totals.items():
        if total < rda[nutrient] * 0.9:
            feedback[nutrient] = f"Low intake of {nutrient}."
        elif total > rda[nutrient] * 1.1:
            feedback[nutrient] = f"High intake of {nutrient}."
        else:
            feedback[nutrient] = f"Good intake of {nutrient}."
    return feedback

from sklearn.linear_model import LinearRegression
import numpy as np

def predict_future_needs(user_history):
    # Example: Predict future calorie needs based on past data
    dates = np.array([i for i in range(len(user_history))]).reshape(-1, 1)
    calories = np.array([day['calories'] for day in user_history])
    
    model = LinearRegression()
    model.fit(dates, calories)
    future_date = np.array([[len(user_history) + 1]])
    predicted_calories = model.predict(future_date)
    return predicted_calories
import matplotlib.pyplot as plt

def plot_nutritional_trends(user_history):
    dates = [day['date'] for day in user_history]
    calories = [day['calories'] for day in user_history]
    proteins = [day['proteins'] for day in user_history]
    
    plt.figure(figsize=(10,5))
    plt.plot(dates, calories, label='Calories')
    plt.plot(dates, proteins, label='Proteins')
    plt.xlabel('Date')
    plt.ylabel('Intake')
    plt.title('Nutritional Trends')
    plt.legend()
    plt.show()
# main.py
from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_food_items, add_user_log
from analysis import calculate_daily_intake, assess_nutrition, get_feedback
from ml_module import generate_recommendations

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/log', methods=['GET', 'POST'])
def log_food():
    if request.method == 'POST':
        user_id = request.form['user_id']
        food_id = request.form['food_id']
        quantity = request.form['quantity']
        unit = request.form['unit']
        add_user_log(user_id, food_id, quantity, unit)
        return redirect(url_for('log_food'))
    food_items = get_food_items()
    return render_template('log_food.html', food_items=food_items)

@app.route('/summary/<user_id>/<date>')
def summary(user_id, date):
    totals = calculate_daily_intake(user_id, date)
    feedback = assess_nutrition(totals)
    recommendations = generate_recommendations(user_id)
    return render_template('summary.html', totals=totals, feedback=feedback, recommendations=recommendations)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('nutritracker.db')
    c = conn.cursor()
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 goal_calories INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS food_items (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 calories INTEGER,
                 proteins REAL,
                 fats REAL,
                 carbohydrates REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_logs (
                 id INTEGER PRIMARY KEY,
                 user_id INTEGER,
                 food_id INTEGER,
                 quantity REAL,
                 unit TEXT,
                 date TEXT,
                 FOREIGN KEY(user_id) REFERENCES users(id),
                 FOREIGN KEY(food_id) REFERENCES food_items(id))''')
    conn.commit()
    conn.close()

def get_food_items():
    conn = sqlite3.connect('nutritracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM food_items")
    items = c.fetchall()
    conn.close()
    return items

def add_user_log(user_id, food_id, quantity, unit):
    conn = sqlite3.connect('nutritracker.db')
    c = conn.cursor()
    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')
    c.execute("INSERT INTO user_logs (user_id, food_id, quantity, unit, date) VALUES (?, ?, ?, ?, ?)",
              (user_id, food_id, quantity, unit, date))
    conn.commit()
    conn.close()
# analysis.py
import sqlite3

def calculate_daily_intake(user_id, date):
    conn = sqlite3.connect('nutritracker.db')
    c = conn.cursor()
    c.execute("""SELECT f.calories, f.proteins, f.fats, f.carbohydrates, l.quantity, l.unit
                 FROM user_logs l
                 JOIN food_items f ON l.food_id = f.id
                 WHERE l.user_id = ? AND l.date = ?""", (user_id, date))
    logs = c.fetchall()
    totals = {'calories': 0, 'proteins': 0, 'fats': 0, 'carbohydrates': 0}
    for log in logs:
        calories, proteins, fats, carbs, quantity, unit = log
        # Assuming unit is in grams for simplicity
        totals['calories'] += calories * quantity / 100
        totals['proteins'] += proteins * quantity / 100
        totals['fats'] += fats * quantity / 100
        totals['carbohydrates'] += carbs * quantity / 100
    conn.close()
    return totals

def assess_nutrition(totals):
    # Example RDA values
    rda = {'calories': 2000, 'proteins': 50, 'fats': 70, 'carbohydrates': 310}
    feedback = {}
    for nutrient, total in totals.items():
        if total < rda[nutrient] * 0.9:
            feedback[nutrient] = f"Low intake of {nutrient}."
        elif total > rda[nutrient] * 1.1:
            feedback[nutrient] = f"High intake of {nutrient}."
        else:
            feedback[nutrient] = f"Good intake of {nutrient}."
    return feedback

# ml_module.py
import sqlite3
from sklearn.linear_model import LinearRegression
import numpy as np

def generate_recommendations(user_id):
    # Fetch user history
    conn = sqlite3.connect('nutritracker.db')
    c = conn.cursor()
    c.execute("""SELECT date, calories, proteins, fats, carbohydrates
                 FROM user_logs l
                 JOIN food_items f ON l.food_id = f.id
                 WHERE l.user_id = ?
                 ORDER BY date""", (user_id,))
    logs = c.fetchall()
    conn.close()
    
    if len(logs) < 5:
        return "Log more meals to get personalized recommendations!"
    
    # Simple recommendation: predict next day's calorie needs
    dates = np.array([i for i in range(len(logs))]).reshape(-1, 1)
    calories = np.array([log[1] for log in logs])
    
    model = LinearRegression()
    model.fit(dates, calories)
    next_day = np.array([[len(logs) + 1]])
    predicted_calories = model.predict(next_day)[0]
    
    # Compare with RDA
    rda_calories = 2000  # Example value
    if predicted_calories < rda_calories * 0.9:
        return "You might need to increase your calorie intake. Consider adding more proteins or healthy fats."
    elif predicted_calories > rda_calories * 1.1:
        return "You're exceeding your calorie goals. Try reducing portion sizes or opting for lower-calorie foods."
    else:
        return "Great job! You're maintaining your calorie intake well."

