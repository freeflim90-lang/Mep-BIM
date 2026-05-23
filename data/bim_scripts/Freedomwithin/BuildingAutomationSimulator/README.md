# Building Energy Management Dashboard

This project is a simplified simulation of a Building Energy Management System (BEMS) dashboard, designed to showcase skills relevant to a Senior Building Automation and Controls Engineer position. It demonstrates the ability to collect, store, process, analyze, and visualize building data.

**Features:**

*   **Data Simulation:** Simulates realistic time-series data for temperature, humidity, and energy consumption (HVAC, lighting, equipment) with daily and weekly patterns.
*   **External Temperature Influence:** Incorporates a simplified model of how external temperature affects internal temperature and HVAC energy use.
*   **Database Storage:** Stores simulated data in an SQLite database.
*   **Data Analysis:** Calculates heating degree days and Energy Use Intensity (EUI).
*   **Web Dashboard:** Provides a user interface to visualize real-time and historical data.
*   **Interactive Chart:** Displays an interactive line chart (using Chart.js) of office temperature over a selectable time period (day, week, month).
*   **Time Range Selection:** Allows users to select the time range for displayed data.

**Technologies Used:**

*   **Python:** For data simulation, database interaction, and backend logic (Flask web framework).
*   **SQLite:** For local database storage.
*   **Flask:** A lightweight Python web framework for creating the dashboard's backend.
*   **HTML, CSS, JavaScript:** For building the frontend dashboard.
*   **Chart.js:** A JavaScript library for creating interactive charts.

## Project Structure:
BuildingAutomationSimulator 
├── README.md
├── app.py
├── building_data.db
├── data_simulator.py
├── requirements.txt
└── templates
    └── index.html
## Setup and Installation:

**Prerequisites:**

*   **Python 3:** Make sure you have Python 3 installed on your system. You can check by running `python3 --version` (macOS/Linux) or `python --version` (Windows) in your terminal.
*   **pip:** `pip` is the package installer for Python. It usually comes installed with Python 3.

**Steps:**

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Freedomwithin/BuildingAutomationSimulator
    cd BuildingAutomationSimulator
    ```

2.  **Create and Activate a Virtual Environment:**

    **Linux/macOS:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

    **Windows (Command Prompt):**

    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

    **Windows (PowerShell):**

    ```bash
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

3.  **Install Dependencies:**

    ```bash
    pip install Flask
    ```

## Running the Application:

1.  **Open two separate terminal windows.**
2.  **In both terminal windows, navigate to the project directory and activate the virtual environment:**

    **Linux/macOS:**

    ```bash
    cd BuildingAutomationSimulator
    source .venv/bin/activate
    ```

    **Windows (Command Prompt):**

    ```bash
    cd BuildingAutomationSimulator
    .venv\Scripts\activate
    ```

    **Windows (PowerShell):**

    ```bash
    cd BuildingAutomationSimulator
    .venv\Scripts\Activate.ps1
    ```

3.  **In the first terminal, start the data simulator:**

    ```bash
    python3 data_simulator.py
    ```

    This script will continuously generate data and store it in the `building_data.db` database.

4.  **In the second terminal, start the Flask application:**

    ```bash
    python3 app.py
    ```

    This will start the web server, making the dashboard accessible in your browser.

5.  **Open your web browser and go to:**

    ```
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
    ```

    You should now see the Building Energy Management Dashboard.
    If you make changes you may need to clear cache in browser or load in an incognito window.

## Future Enhancements:

*   **Alerting:** Implement alerts for sensor values exceeding thresholds.
*   **More Dashboard Customization:** Allow users to select which zones/sensors to display.
*   **Authentication:** Add a login system to secure the dashboard.
*   **Deployment:** Deploy the application to a cloud platform (e.g., Heroku, PythonAnywhere).
*   **Real-time Weather Data:** Integrate a weather API to use real-time external temperature data.

## Author

Freedomwithin/Jonathon K.

## Acknowledgments

*   Chart.js: [https://www.chartjs.org/](https://www.chartjs.org/)
*   Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)

