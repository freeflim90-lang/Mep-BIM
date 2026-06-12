import numpy as np
import matplotlib.pyplot as plt
import math
import csv

def read_csv(filename,col):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row

        # Iterate over the rows and retrieve the second column
        second_column_values = []
        for row in csv_reader:
            second_column_values.append(float(row[col]))

    return second_column_values

energy_all=[]
#Declare Variable
c_air = 1005 #J/(kg*k)
w_air = 1.225 #weight air (kg)
absorbability = 0.1
#Glass
shgc = 0.26
U_value = 0.24

time = 1440 #min

desired_temp=20 #degree c

data_temp = read_csv("/Users/tew/Downloads/22.3034, 114.1602 2022-01-01 to 2022-12-31.csv",3)
data_solar_radiation = read_csv("/Users/tew/Downloads/22.3034, 114.1602 2022-01-01 to 2022-12-31.csv",17)

note = 0
note_temp = 0
note_solar =0
def moving_average(data, window_size=10):
    window = np.ones(window_size) / window_size
    smoothed_data = np.convolve(data, window, mode='same')
    return smoothed_data
print(len(data_temp), len(data_solar_radiation))
for d in range(365):
    outside_temp = []
    solar_radiation = []
    for i in range(24):
        for _ in range(60):
            outside_temp.append(data_temp[d*24+i])
            solar_radiation.append(data_solar_radiation[d*24+i])
            
    outside_temp=moving_average(outside_temp)
    solar_radiation=moving_average(solar_radiation)
    
    
    #Parameter of the room in meter
    x_size = 60
    y_size = 484
    
    energy_day=[]

    U = 0.24
    
    
    #get outside temp, solar radiation for every min
    for t in range(time):
        
        energy=absorbability*shgc*solar_radiation[t]*x_size*y_size #J
        
        energy+=U*(outside_temp[t]-desired_temp)*2*y_size*x_size #J
        energy= energy/1000
        
        energy= energy/4.7
        energy_day.append(energy)
        
        
    note_temp+= sum(outside_temp)
    note_solar += sum (solar_radiation)
    note +=sum(energy_day)
    #energy_all.append(energy_day)
    if d in [30, 58, 89, 119, 150, 180, 211, 242, 272, 303, 333, 364]:
        print(note, note_temp, note_solar)
        note, note_temp, note_solar = 0


    
"""
from scipy.signal import savgol_filter

# Choose polynomial degree (usually 3 or 5)
polynomial_degree = 3

def savgol_smooth(data, window_size, poly_degree):
  smoothed = savgol_filter(data, window_size, poly_degree)
  return smoothed

# Select smoothing method (uncomment desired function)
# smoothed_data = moving_average(temperature, window_size)
smoothed_data = savgol_smooth(energy_day, 100, 3)

# Plot original and smoothed data
plt.plot(energy_day, label='Original')
plt.plot(smoothed_data, label='Smoothed')
plt.xlabel('Time (minutes)')
plt.ylabel('Temperature')
plt.legend()
plt.grid(True)
plt.show()
"""
