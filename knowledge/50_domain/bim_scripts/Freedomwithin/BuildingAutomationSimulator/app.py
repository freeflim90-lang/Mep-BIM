from flask import Flask, render_template, jsonify, request
import sqlite3
import datetime

DATABASE = 'building_data.db'

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_degree_days(temperatures, base_temperature=18):
    """Calculates heating degree days."""
    degree_days = 0
    for temp in temperatures:
        degree_days += max(0, base_temperature - temp)
    return degree_days

def calculate_eui(energy_consumption, area=1000):  # Assume 1000 sq ft if not provided
    """Calculates Energy Use Intensity (EUI)."""
    return energy_consumption / area

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    period = request.args.get('period', 'day')  # Get period from query parameter, default to 'day'
    conn = get_db_connection()
    cursor = conn.cursor()

    # Time filter for data retrieval
    if period == 'day':
        time_filter = datetime.datetime.now() - datetime.timedelta(days=1)
    elif period == 'week':
        time_filter = datetime.datetime.now() - datetime.timedelta(days=7)
    elif period == 'month':
        time_filter = datetime.datetime.now() - datetime.timedelta(days=30)
    else:
        time_filter = datetime.datetime.now() - datetime.timedelta(days=1) #default to day

    # Example: Fetch temperatures and timestamps for the selected period
    cursor.execute('''
        SELECT strftime('%Y-%m-%d %H:%M:%S', r.timestamp), r.value
        FROM readings r
        JOIN sensors s ON r.sensor_id = s.sensor_id
        WHERE s.sensor_type = 'temperature' AND s.location = 'office' AND r.timestamp >= ?
        ORDER BY r.timestamp
    ''', (time_filter,))
    temp_data = cursor.fetchall()

    timestamps = [row[0] for row in temp_data]
    temperatures = [row[1] for row in temp_data]

    # Get latest temperature for each location
    cursor.execute('''
        SELECT s.location, r.value, r.timestamp 
        FROM readings r
        JOIN sensors s ON r.sensor_id = s.sensor_id
        WHERE s.sensor_type = 'temperature'
        AND r.reading_id IN (SELECT MAX(reading_id) FROM readings GROUP BY sensor_id)
    ''')
    temperatures_display = [{'location': row['location'], 'value': row['value'], 'timestamp': row['timestamp']} for row in cursor.fetchall()]

    cursor.execute('''
        SELECT s.location, r.value, r.timestamp 
        FROM readings r
        JOIN sensors s ON r.sensor_id = s.sensor_id
        WHERE s.sensor_type = 'humidity'
        AND r.reading_id IN (SELECT MAX(reading_id) FROM readings GROUP BY sensor_id)
    ''')
    humidity = [{'location': row['location'], 'value': row['value'], 'timestamp': row['timestamp']} for row in cursor.fetchall()]

    cursor.execute('''
        SELECT s.location, SUM(r.value) as total_consumption
        FROM readings r
        JOIN sensors s ON r.sensor_id = s.sensor_id
        WHERE s.sensor_type = 'energy_consumption' AND r.timestamp >= ?
        GROUP BY s.location
    ''', (time_filter,))

    energy_consumption = [{'location': row['location'], 'total_consumption': row['total_consumption']} for row in cursor.fetchall()]

    # Calculate degree days (using office temperature for simplicity)
    degree_days = calculate_degree_days(temperatures)

    # Calculate total energy consumption for EUI calculation
    cursor.execute('''
        SELECT SUM(r.value) as total_consumption
        FROM readings r
        JOIN sensors s ON r.sensor_id = s.sensor_id
        WHERE s.sensor_type = 'energy_consumption' AND r.timestamp >= ?
    ''', (time_filter,))
    total_energy = cursor.fetchone()['total_consumption']

    # Calculate EUI
    eui = calculate_eui(total_energy)

    conn.close()

    return jsonify({
        'timestamps': timestamps,
        'temperatures': temperatures,
        'temperatures_display': temperatures_display,
        'humidity': humidity,
        'energy_consumption': energy_consumption,
        'degree_days': degree_days,
        'eui': eui
    })

if __name__ == '__main__':
    app.run(debug=True)
