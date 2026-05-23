import sqlite3
import time
import random
import datetime

DATABASE = 'building_data.db'

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_type TEXT,
            location TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER,
            timestamp DATETIME,
            value REAL,
            FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
        )
    ''')
    conn.commit()

def get_last_hvac_energy(conn):
    """Retrieves the most recent HVAC energy consumption value."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.value
        FROM readings r
        JOIN sensors s ON r.sensor_id = s.sensor_id
        WHERE s.sensor_type = 'energy_consumption' AND s.location = 'HVAC'
        ORDER BY r.timestamp DESC
        LIMIT 1
    ''')
    result = cursor.fetchone()
    return result[0] if result else 0

def get_external_temperature(hour, day_of_week):
    """Simulates external temperature based on time of day and day of week."""
    if day_of_week < 5:  # Weekday
        if 6 <= hour <= 18:
            return random.uniform(15, 25)  # Daytime
        else:
            return random.uniform(10, 15)  # Nighttime
    else:  # Weekend
        if 8 <= hour <= 20:
            return random.uniform(14, 24)  # Daytime
        else:
            return random.uniform(9, 14)  # Nighttime

def insert_sensor_data(conn, sensor_type, location, value):
    cursor = conn.cursor()

    # Check if the sensor exists
    cursor.execute("SELECT sensor_id FROM sensors WHERE sensor_type = ? AND location = ?", (sensor_type, location))
    sensor = cursor.fetchone()

    if sensor is None:
        # Insert the new sensor
        cursor.execute("INSERT INTO sensors (sensor_type, location) VALUES (?, ?)", (sensor_type, location))
        sensor_id = cursor.lastrowid
    else:
        sensor_id = sensor[0]

    # Get the last temperature reading for influence calculation
    if sensor_type == 'temperature':
        cursor.execute('''
            SELECT value FROM readings
            WHERE sensor_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (sensor_id,))
        last_temp_reading = cursor.fetchone()
        previous_temperature = last_temp_reading[0] if last_temp_reading else value

        external_temp = get_external_temperature(datetime.datetime.now().hour, datetime.datetime.now().weekday())
        hvac_energy = get_last_hvac_energy(conn)

        # Influence calculations
        temperature_influence = (external_temp - 21) * 0.2
        hvac_influence = hvac_energy * -0.5

        # Calculate new temperature
        value = previous_temperature + temperature_influence + hvac_influence
        value = max(min(value, 25), 18)  # Keep within reasonable bounds

    # Insert the reading
    timestamp = datetime.datetime.now()
    cursor.execute("INSERT INTO readings (sensor_id, timestamp, value) VALUES (?, ?, ?)", (sensor_id, timestamp, value))
    conn.commit()

def simulate_data(conn):
    while True:
        hour = datetime.datetime.now().hour
        day_of_week = datetime.datetime.now().weekday()

        # Office Temperature
        insert_sensor_data(conn, 'temperature', 'office', 0)
        # Office Humidity
        insert_sensor_data(conn, 'humidity', 'office', random.uniform(40, 60))

        # Server Room Temperature
        insert_sensor_data(conn, 'temperature', 'server_room', 0)
        # Server Room Humidity
        insert_sensor_data(conn, 'humidity', 'server_room', random.uniform(30, 50))

        # Lobby Temperature
        insert_sensor_data(conn, 'temperature', 'lobby', 0)
        # Lobby Humidity
        insert_sensor_data(conn, 'humidity', 'lobby', random.uniform(45, 65))

        # HVAC Energy Consumption
        if day_of_week < 5:  # Weekday
            if 7 <= hour <= 19:
                hvac_energy = random.uniform(8, 15)
            else:
                hvac_energy = random.uniform(4, 8)
        else:  # Weekend
            if 9 <= hour <= 21:
                hvac_energy = random.uniform(6, 12)
            else:
                hvac_energy = random.uniform(3, 6)
        insert_sensor_data(conn, 'energy_consumption', 'HVAC', hvac_energy)

        # Lighting Energy Consumption
        if 6 <= hour <= 20:
            lighting_energy = random.uniform(3, 7)
        else:
            lighting_energy = random.uniform(1, 3)
        insert_sensor_data(conn, 'energy_consumption', 'Lighting', lighting_energy)

        # Equipment Energy Consumption
        if 8 <= hour <= 18:
            equipment_energy = random.uniform(5, 10)
        else:
            equipment_energy = random.uniform(2, 5)
        insert_sensor_data(conn, 'energy_consumption', 'Equipment', equipment_energy)

        print("Data inserted...")
        time.sleep(300)  # Simulate data every 5 minutes

if __name__ == "__main__":
    conn = sqlite3.connect(DATABASE)
    create_tables(conn)
    simulate_data(conn)
    conn.close()
