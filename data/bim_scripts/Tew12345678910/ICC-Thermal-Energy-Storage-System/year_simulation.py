import numpy as np
import matplotlib.pyplot as plt
import math
import csv
from datetime import datetime, timedelta
import os

def read_csv(filename, col):
    """Read specific column from CSV file"""
    if not os.path.exists(filename):
        print(f"Warning: Weather data file '{filename}' not found.")
        print("Using synthetic data for demonstration...")
        return generate_synthetic_data()
    
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        # Iterate over the rows and retrieve the specified column
        column_values = []
        for row in csv_reader:
            if len(row) > col:
                try:
                    column_values.append(float(row[col]))
                except ValueError:
                    column_values.append(0.0)  # Default value for invalid data
            else:
                column_values.append(0.0)  # Default value for missing data

    return column_values

def generate_synthetic_data():
    """Generate synthetic weather data for demonstration when real data is not available"""
    np.random.seed(42)
    data = []
    for day in range(365):
        for hour in range(24):
            # Simulate Hong Kong weather patterns
            base_temp = 25 + 5 * np.sin(2 * np.pi * day / 365)  # Seasonal variation
            daily_variation = 3 * np.sin(2 * np.pi * hour / 24)  # Daily variation
            noise = np.random.normal(0, 1)  # Random fluctuation
            temp = base_temp + daily_variation + noise
            data.append(max(15, min(35, temp)))  # Clamp between reasonable values
    return data

def generate_synthetic_solar_data():
    """Generate synthetic solar radiation data"""
    np.random.seed(43)
    data = []
    for day in range(365):
        for hour in range(24):
            if 6 <= hour <= 18:  # Daylight hours
                base_radiation = 800 * np.sin(np.pi * (hour - 6) / 12)  # Peak at noon
                seasonal_factor = 0.8 + 0.4 * np.sin(2 * np.pi * day / 365)
                noise = np.random.normal(0, 50)
                radiation = max(0, base_radiation * seasonal_factor + noise)
            else:
                radiation = 0
            data.append(radiation)
    return data

# Initialize variables
energy_all = []
daily_totals = []
monthly_totals = []
tes_savings = []

# Declare Physical Constants and Building Parameters
c_air = 1005  # Specific heat of air (J/(kg*K))
rho_air = 1.225  # Air density (kg/m³)
absorbability = 0.1  # Building absorption coefficient
# Glass properties
shgc = 0.26  # Solar Heat Gain Coefficient
U_value = 0.24  # Heat transfer coefficient (W/(m²*K))

# TES System Parameters
tes_capacity = 5000000  # TES capacity in Joules (5 MJ)
tes_efficiency = 0.85  # TES charge/discharge efficiency
tes_stored_energy = 0  # Current stored energy
tes_max_charge_rate = 1000000  # Maximum charge rate (1 MW)
tes_max_discharge_rate = 1000000  # Maximum discharge rate (1 MW)

# Simulation parameters
time_minutes = 1440  # Minutes in a day
x_size = 60  # Building width (m)
y_size = 484  # Building height (m) - ICC height

# Load weather data
print("Loading weather data...")
try:
    data_temp = read_csv("weather_data.csv", 3)  # Generic filename for temperature
    data_solar_radiation = read_csv("weather_data.csv", 17)  # Generic filename for solar radiation
except:
    print("Using synthetic weather data...")
    data_temp = generate_synthetic_data()
    data_solar_radiation = generate_synthetic_solar_data()

print(f"Loaded {len(data_temp)} temperature data points and {len(data_solar_radiation)} solar radiation data points")

def setup_gradient_air(x_size, y_size, initial_temp):
    """Initialize temperature gradient matrix"""
    temp_grad = [[initial_temp for _ in range(x_size)] for _ in range(y_size)]
    return temp_grad

def calculate_tes_operation(energy_demand, tes_stored, capacity, max_charge, max_discharge, efficiency):
    """Calculate TES charge/discharge based on energy demand"""
    if energy_demand > 0:  # Need cooling/heating
        # Try to discharge from TES
        discharge_amount = min(energy_demand, max_discharge, tes_stored * efficiency)
        tes_stored -= discharge_amount / efficiency
        remaining_demand = energy_demand - discharge_amount
        return tes_stored, remaining_demand, discharge_amount
    else:  # Excess energy available
        # Try to charge TES
        excess_energy = abs(energy_demand)
        charge_amount = min(excess_energy, max_charge, (capacity - tes_stored) / efficiency)
        tes_stored += charge_amount * efficiency
        return tes_stored, 0, -charge_amount

# Main simulation loop
print("\nStarting year-long simulation...")
print("This may take several minutes...")

for d in range(365):
    if d % 30 == 0:  # Progress update every 30 days
        print(f"Processing day {d+1}/365...")
    
    # Prepare daily temperature and solar radiation data
    outside_temp = []
    solar_radiation = []
    
    # Extract hourly data for the day and interpolate to minutes
    for i in range(24):
        temp_index = min(d * 24 + i, len(data_temp) - 1)
        solar_index = min(d * 24 + i, len(data_solar_radiation) - 1)
        
        for _ in range(60):  # Convert hourly to minute data
            outside_temp.append(data_temp[temp_index])
            solar_radiation.append(data_solar_radiation[solar_index])
    
    energy_day = []
    daily_tes_savings = 0
    
    # Initialize temperature gradient for the day
    initial_temp = outside_temp[0]
    temp1 = setup_gradient_air(x_size, y_size, initial_temp)
    
    # Minute-by-minute simulation for the day
    for t in range(time_minutes):
        # Solar radiation effects
        if solar_radiation[t] > 0.0:
            # East-facing wall (morning sun)
            for y in range(y_size):
                temp1[y][0] += solar_radiation[t] * absorbability
        
        # Heat transfer through building envelope (U-value effects)
        U = U_value
        for y in range(y_size):
            # Heat transfer through exterior walls
            temp1[y][0] += U * (outside_temp[t] - temp1[y][0]) * 60 / (c_air * rho_air)
            temp1[y][x_size-1] += U * (outside_temp[t] - temp1[y][x_size-1]) * 60 / (c_air * rho_air)
        
        # Internal air circulation simulation (simplified finite difference)
        temp2 = setup_gradient_air(x_size, y_size, initial_temp)
        
        dl = 1.0  # Grid size (m)
        dt = 60.0  # Time step (seconds)
        thermal_diffusivity = 0.02  # Air thermal diffusivity (m²/s)
        
        # Apply heat diffusion equation
        for y in range(1, y_size - 1):
            for x in range(1, x_size - 1):
                dd_temp_y = (temp1[y+1][x] + temp1[y-1][x] - 2 * temp1[y][x])
                dd_temp_x = (temp1[y][x+1] + temp1[y][x-1] - 2 * temp1[y][x])
                temp2[y][x] = thermal_diffusivity * dt / (dl**2) * (dd_temp_x + dd_temp_y) + temp1[y][x]
        
        temp1 = [row[:] for row in temp2]  # Deep copy
        
        # Calculate energy demand for this minute
        solar_energy = absorbability * shgc * solar_radiation[t] * 60 * x_size
        
        envelope_energy = 0
        for y in range(y_size):
            envelope_energy += x_size * U * (temp1[y][0] - outside_temp[t]) * 60
            envelope_energy += x_size * U * (temp1[y][x_size-1] - outside_temp[t]) * 60
        
        total_energy = solar_energy + envelope_energy
        
        # Apply TES system
        tes_stored_energy, remaining_demand, tes_contribution = calculate_tes_operation(
            total_energy, tes_stored_energy, tes_capacity, 
            tes_max_charge_rate, tes_max_discharge_rate, tes_efficiency
        )
        
        final_energy = remaining_demand
        daily_tes_savings += abs(tes_contribution)
        
        energy_day.append(final_energy)
    
    # Store daily results
    energy_all.append(energy_day)
    daily_total = sum(energy_day)
    daily_totals.append(daily_total)
    tes_savings.append(daily_tes_savings)
    
    # Calculate monthly totals
    if (d + 1) % 30 == 0 or d == 364:  # End of month or year
        month_start = max(0, d - 29)
        monthly_total = sum(daily_totals[month_start:d+1])
        monthly_totals.append(monthly_total)

print("Simulation completed!")

# Data Analysis and Results
print("\n" + "="*50)
print("YEAR-LONG ICC ENERGY ANALYSIS RESULTS")
print("="*50)

# Calculate statistics
total_energy_year = sum(daily_totals)
avg_daily_energy = total_energy_year / 365
max_daily_energy = max(daily_totals)
min_daily_energy = min(daily_totals)
total_tes_savings_year = sum(tes_savings)

print(f"\nEnergy Consumption Statistics:")
print(f"Total Annual Energy: {total_energy_year/1e9:.2f} GJ")
print(f"Average Daily Energy: {avg_daily_energy/1e6:.2f} MJ")
print(f"Maximum Daily Energy: {max_daily_energy/1e6:.2f} MJ")
print(f"Minimum Daily Energy: {min_daily_energy/1e6:.2f} MJ")
print(f"Energy Range: {(max_daily_energy - min_daily_energy)/1e6:.2f} MJ")

print(f"\nThermal Energy Storage (TES) Benefits:")
print(f"Total TES Savings: {total_tes_savings_year/1e9:.2f} GJ")
print(f"Average Daily TES Savings: {total_tes_savings_year/365/1e6:.2f} MJ")
print(f"TES Efficiency Impact: {(total_tes_savings_year/total_energy_year)*100:.1f}% energy reduction")

# Environmental Impact
co2_factor = 0.5  # kg CO2 per MJ (approximate for Hong Kong electricity)
co2_savings = total_tes_savings_year * co2_factor / 1e6  # Convert to tonnes
print(f"\nEnvironmental Impact:")
print(f"Estimated CO2 Reduction: {co2_savings:.1f} tonnes/year")

# Save detailed results to CSV
print("\nSaving results to CSV files...")

# Daily summary
with open('year_simulation_daily_results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Day', 'Date', 'Total_Energy_MJ', 'TES_Savings_MJ', 'Net_Energy_MJ'])
    
    start_date = datetime(2022, 1, 1)
    for i, (daily_total, tes_saving) in enumerate(zip(daily_totals, tes_savings)):
        date = start_date + timedelta(days=i)
        net_energy = daily_total - tes_saving
        writer.writerow([
            i+1, 
            date.strftime('%Y-%m-%d'), 
            daily_total/1e6, 
            tes_saving/1e6, 
            net_energy/1e6
        ])

# Monthly summary
with open('year_simulation_monthly_results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Month', 'Total_Energy_GJ', 'Avg_Daily_Energy_MJ'])
    
    for i, monthly_total in enumerate(monthly_totals):
        days_in_period = 30 if i < len(monthly_totals) - 1 else (365 % 30) or 30
        avg_daily = monthly_total / days_in_period
        writer.writerow([i+1, monthly_total/1e9, avg_daily/1e6])

print("Results saved to 'year_simulation_daily_results.csv' and 'year_simulation_monthly_results.csv'")

# Create visualizations
print("\nGenerating visualizations...")

# Create figure with subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('ICC Building - Year-Long Energy Analysis with TES', fontsize=16, fontweight='bold')

# Plot 1: Daily Energy Consumption Over the Year
days = range(1, 366)
ax1.plot(days, [e/1e6 for e in daily_totals], 'b-', linewidth=1, label='Daily Energy')
ax1.plot(days, [e/1e6 for e in tes_savings], 'g-', linewidth=1, label='TES Savings')
ax1.set_xlabel('Day of Year')
ax1.set_ylabel('Energy (MJ)')
ax1.set_title('Daily Energy Consumption and TES Savings')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Monthly Energy Totals
months = range(1, len(monthly_totals) + 1)
ax2.bar(months, [m/1e9 for m in monthly_totals], color='skyblue', alpha=0.7)
ax2.set_xlabel('Month')
ax2.set_ylabel('Energy (GJ)')
ax2.set_title('Monthly Energy Consumption')
ax2.grid(True, alpha=0.3)

# Plot 3: Energy Distribution Histogram
ax3.hist([e/1e6 for e in daily_totals], bins=30, color='lightcoral', alpha=0.7, edgecolor='black')
ax3.set_xlabel('Daily Energy (MJ)')
ax3.set_ylabel('Frequency (Days)')
ax3.set_title('Distribution of Daily Energy Consumption')
ax3.grid(True, alpha=0.3)

# Plot 4: TES Impact Analysis
net_energy = [daily - saving for daily, saving in zip(daily_totals, tes_savings)]
ax4.plot(days, [e/1e6 for e in daily_totals], 'r-', linewidth=2, label='Without TES')
ax4.plot(days, [e/1e6 for e in net_energy], 'g-', linewidth=2, label='With TES')
ax4.fill_between(days, [e/1e6 for e in daily_totals], [e/1e6 for e in net_energy], 
                alpha=0.3, color='green', label='TES Savings')
ax4.set_xlabel('Day of Year')
ax4.set_ylabel('Energy (MJ)')
ax4.set_title('TES Impact on Energy Consumption')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('year_simulation_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Create seasonal analysis
print("\nGenerating seasonal analysis...")

# Define seasons (for Hong Kong)
spring_days = daily_totals[59:151]   # Mar-May
summer_days = daily_totals[151:244]  # Jun-Aug  
autumn_days = daily_totals[244:334]  # Sep-Nov
winter_days = daily_totals[334:] + daily_totals[:59]  # Dec-Feb

seasonal_avgs = [
    sum(spring_days)/len(spring_days)/1e6,
    sum(summer_days)/len(summer_days)/1e6,
    sum(autumn_days)/len(autumn_days)/1e6,
    sum(winter_days)/len(winter_days)/1e6
]

# Seasonal plot
plt.figure(figsize=(10, 6))
seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
colors = ['lightgreen', 'orange', 'brown', 'lightblue']
bars = plt.bar(seasons, seasonal_avgs, color=colors, alpha=0.7, edgecolor='black')
plt.ylabel('Average Daily Energy (MJ)')
plt.title('Seasonal Energy Consumption - ICC Building')
plt.grid(True, alpha=0.3)

# Add value labels on bars
for bar, value in zip(bars, seasonal_avgs):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(seasonal_avgs)*0.01,
             f'{value:.1f} MJ', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('seasonal_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*50)
print("SIMULATION COMPLETE")
print("="*50)
print("Files generated:")
print("- year_simulation_daily_results.csv")
print("- year_simulation_monthly_results.csv") 
print("- year_simulation_analysis.png")
print("- seasonal_analysis.png")
print("\nThe simulation demonstrates the significant benefits of")
print("implementing Thermal Energy Storage systems in the ICC building")
print("for achieving greener, more sustainable HVAC operations.")
print("="*50)