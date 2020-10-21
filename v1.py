#By Beau Hodes
#Speech sensor, CAFET based

import time
import math
import matplotlib.pyplot as plt
from gdx import gdx
import pyaudio
import wave
import audioop
from collections import deque

#------------------------------VOICE SET UP------------------------------------
CHUNK = 2048  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 7000  # The threshold intensity that defines silence
WINDOW_LENGTH = 1
#---------------------------------END VOICE SETUP------------------------------

#------------------------------PLOT SET UP-------------------------------------
gdx = gdx.gdx()

fig, ax = plt.subplots()

time_between_readings_in_seconds = 0.1
number_of_readings = 200
digits_of_precision = 2

period_in_ms = time_between_readings_in_seconds*1000

gdx.open_usb()
gdx.select_sensors([1])

column_headers = gdx.enabled_sensor_info() #confirm name of measurement taken ("Force (N)")
column_headers_string = str(column_headers)
column_headers_string = column_headers_string.replace("'","")
column_headers_string = column_headers_string.replace("[","")
column_headers_string = column_headers_string.replace("]","")

sensor_times=[]
sensor_readings=[]
print_table_string = []
#---------------------------------END PLOT SETUP------------------------------

plt.pause(1)
gdx.start(period_in_ms)

def plot_graph(time):
    #Using pyplot
    ax.plot(sensor_times,sensor_readings, color='k',label=column_headers[0])

    plt.ylabel(column_headers_string) #name and units of the sensor selected#
    plt.xlabel('Time(s)')
    plt.axis([sensor_times[0] - 2, sensor_times[-1] + 7, 0, 24])
    plt.grid(False) #This controls whether there is a grid on the graph
    plt.pause (0.05) # display the graph briefly, as the readings are taken

#plots two lines after prevoice
def plot_prevoice():
    plt.plot([sensor_times[-1] + .5, sensor_times[-1] + .5], [0, 24], 'k-', lw=1)
    plt.plot([sensor_times[-1] + .9, sensor_times[-1] + .9], [0, 24], 'k-', lw=1)

def plot_voiceOn():
    plt.title('Voice: ---', loc='right')

def plot_voiceOff():
    plt.title('Voice:    ', loc='right')


#terminal setup (for testing)
def print_table():
    print ("Data Table:")
    print ('Time (s) ',column_headers_string) #label the data table that will be printed on the Python Shell

    # The print_table_string is a list of strings. Each element in the list contains the time and readings.
    # This variable is created in the Data Collection loop.
    for string in print_table_string:
        print(string)

#data collection
collection_complete = False
removeData = False
pvPause = True
isRising = False
pauseTimer = 0
delayed_slope = 0

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input_device_index = 0,
                input=True,
                frames_per_buffer=CHUNK)
cur_data = '' # current chunk  of audio data
rel = (RATE/CHUNK)
slid_win = deque(maxlen=int(WINDOW_LENGTH * rel)) #use a sliding window

while not collection_complete:
    try:
        time = 0
        print ('Collecting Data...')

        # Print the column headers in terminal
        print('Time(s), ' + column_headers_string)

        for i in range(0,number_of_readings):

            # Create a list of times to be used in the graph and data table
            sensor_times.append(time)
            if(time > 3):
                sensor_times.pop(0)
                removeData = True

            # Read the list of measurements from the sensor
            measurements=gdx.read()
            if measurements == None:
                break

            # Store each sensor's measurement in a list to be used in plot_graph() and print_table()
            data_string = ''
            for data in measurements:
                sensor_readings.append(data)
                if(removeData == True):
                    sensor_readings.pop(0)
                    delayed_slope = (sensor_readings[-1] - sensor_readings[-3]) / (sensor_times[-1] - sensor_times[-3])#y2-y1 / x2-x1
                    print('cur slope: ', delayed_slope)

                # Build a string for printing to the terminal
                round_data = str(round(data,digits_of_precision))
                data_string = data_string + round_data + '   '

            # Print the time and the data to the terminal
            print(str(round(time,2)) + '   '+ data_string)

            # If the last reading is finished update the graph's title
            if  i >=number_of_readings-1:
                plt.title(column_headers_string +' vs '+'Time (s)')

            # Call the plot_graph() function to update the graph with the new data set.
            plot_graph(time)

            #deal with prevoice lines
            if((time - pauseTimer) > 2):
                pvPause = False
            if(delayed_slope > 0 and sensor_readings[-1] > 7):
                isRising = True
            if(delayed_slope < 0):
                isRising = False
            if(delayed_slope < 1.5 and isRising == True and pvPause == False):
                plot_prevoice()
                pvPause = True
                isRising = False
                pauseTimer = time

            #deal with voice bar
            cur_data = stream.read(CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            if(sum([x > THRESHOLD for x in slid_win]) > 0):
                plot_voiceOn()
            else:
                plot_voiceOff()

            # Update the time variable with the new time for the next data point
            time = time+time_between_readings_in_seconds

        # The data collection loop is finished
        collection_complete=True
        print ('data  collection complete')
        print ('Number of readings: ',i+1)
        print ('Time between readings: ',time_between_readings_in_seconds, " s")
        print ('Total time for data collection ', time, ' s')

        # Stop sensor readings and disconnect the device.
        gdx.stop()
        gdx.close()


    except KeyboardInterrupt:
        collection_complete=True
        gdx.stop() #stop sensor readings
        gdx.close()#disconnect the device
        stream.close() #stop voice stream
        p.terminate() #terminate pyaudio object
        print ('data  collection stopped by keypress')
        print ('Number of readings: ',i+1)

# Command to leave the graph window open when the program ends.
plt.show()
