import numpy as np
import matplotlib.pyplot as plt
import math

def moving_average(data, window_size=10):
    window = np.ones(window_size) / window_size
    smoothed_data = np.convolve(data, window, mode='same')
    return smoothed_data

#Declare Variable
c_air = 1005 #J/(kg*k)
w_air = 1.225 #weight air (kg)
absorbability = 0.5
#Glass
shgc = 0.26
U_value = 0.24

time = 1440 #min

data_temp = [22.9, 22.8, 21.3, 22, 22, 21, 21.9, 21.9, 21.1, 23.1, 23.3, 21.6, 24.1, 24.8, 23.6, 25.4, 24.5, 22.9, 23.7, 22.7, 21.6, 22.5, 22.9, 21.7] #degree celsius
data_solar_radiation = [0, 0, 0, 0, 0, 0, 0, 1, 12, 175, 245, 326, 435, 524, 568, 729, 643, 541, 441, 355, 296, 0, 0, 0]
outside_temp = []
solar_radiation = []

#get outside temp, solar radiation for every min
for t in range(time):
    i = int(t/60)
    outside_temp.append(data_temp[i])
    #+ in east, - in west side
    solar_radiation.append(data_solar_radiation[i])
solar_radiation= moving_average(solar_radiation)

solar_radiation= solar_radiation*absorbability*shgc*60/(c_air*w_air)

for i in range(721,1440):
    solar_radiation[i]=solar_radiation[i]*-1


#Parameter of the room in meter
x_size = 60
y_size = 484





def setup_gradient_air():
    temp_grad = [[outside_temp[0] for _ in range(x_size)] for _ in range(y_size)]
    return temp_grad


temp1 = setup_gradient_air()

fig2, axis2 = plt.subplots()
room = axis2.pcolormesh(temp1, cmap = plt.cm.jet, vmin = 20, vmax = 40)
plt.colorbar(room, ax=axis2)


plt.pause(20)
for t in range(time):
    #sun radiation
    
    print(solar_radiation[t]) 
    if solar_radiation[t] > 0.0:
        for y in range(y_size):
            temp1[y][0] += solar_radiation[t]
    elif solar_radiation[t] < 0.0:
        for y in range(y_size):
            temp1[y][x_size-1] += solar_radiation[t]*-1
    
    
    #Heat transfer (U value)
    U=0.24
    
    for y in range(y_size):
        temp1[y][0]+=U*(temp1[y][0]-outside_temp[t])*60/c_air*w_air
        temp1[y][x_size-1]+=U*(temp1[y][x_size-1]-outside_temp[t])*60/c_air*w_air
    #Air
    
    temp2 = setup_gradient_air()
    
    dl = 1 #size of block
    dt = 0.1 #sec
    c_air = 2.5
    
    
    for y in range(1,y_size-1):
        for x in range(1,x_size-1):
            dd_temp_y = (temp1[y+1][x])+(temp1[y-1][x])-2*(temp1[y][x])
            dd_temp_x = (temp1[y][x+1])+(temp1[y][x-1])-2*(temp1[y][x])
            temp2[y][x] = c_air * dt/(dl**2) * (dd_temp_x+dd_temp_y) + temp1[y][x]

    temp1 = temp2.copy()
    

    
    
    room.set_array(temp1)
    
    axis2.set_title(f"t = {t}min")
    
    plt.pause(0.0001)
plt.show()


