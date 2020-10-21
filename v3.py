#By Beau Hodes
#Speech sensor, CAFET based
#v3, using threading
#try only updating the plot DATA in the second thread. do all plotting in main thread since it is a loop
#try not using mainloop but use window.update

import time
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from gdx import gdx
import pyaudio
import wave
import audioop
from collections import deque
import tkinter as tk
from tkinter import ttk
from threading import Thread


#----------------------------general setup----------------------------------
LARGE_FONT = ("Verdana", 12)
style.use("dark_background")
gdx = gdx.gdx()
#----------------------------------------------------------------------------
sensor_times=[]
sensor_readings=[]
column_headers = []
column_headers_string = ""
fig, ax = plt.subplots()
#----------------------------------------------------------------------------




#test
#---------------------------sensor setup-------------------------------------
gdx.open_usb()
gdx.select_sensors([1])
#----------------------------------------------------------------------------

#---------------------------microphone setup---------------------------------

#----------------------------------------------------------------------------

#----------------------------variable setup---------------------------------
time_between_readings_in_seconds = 0.1
#number_of_readings = 1000
number_of_readings = 100
digits_of_precision = 2
period_in_ms = time_between_readings_in_seconds*1000

column_headers = gdx.enabled_sensor_info() #confirm name of measurement taken ("Force (N)")
column_headers_string = str(column_headers)
column_headers_string = column_headers_string.replace("'","")
column_headers_string = column_headers_string.replace("[","")
column_headers_string = column_headers_string.replace("]","")

sensor_times=[]
sensor_readings=[]
column_headers = []
column_headers_string = ""
fig, ax = plt.subplots()

#data collection
collection_complete = False
removeData = False
pvPause = True
isRising = False
pauseTimer = 0
delayed_slope = 0
#end test

def animate(i):
    collectAndPlot(i)

def collectAndPlot(i):
    global sensor_readings
    global sensor_times
    global column_headers
    global column_headers_string
    global gdx
    #---------------------------sensor setup-------------------------------------
    gdx.open_usb()
    gdx.select_sensors([1])
    #----------------------------------------------------------------------------

    #---------------------------microphone setup---------------------------------

    #----------------------------------------------------------------------------

    #----------------------------variable setup---------------------------------
    time_between_readings_in_seconds = 0.1
    #number_of_readings = 1000
    number_of_readings = 100
    digits_of_precision = 2
    period_in_ms = time_between_readings_in_seconds*1000

    column_headers = gdx.enabled_sensor_info() #confirm name of measurement taken ("Force (N)")
    column_headers_string = str(column_headers)
    column_headers_string = column_headers_string.replace("'","")
    column_headers_string = column_headers_string.replace("[","")
    column_headers_string = column_headers_string.replace("]","")

    sensor_times=[]
    sensor_readings=[]
    print_table_string = []

    #data collection
    collection_complete = False
    removeData = False
    pvPause = True
    isRising = False
    pauseTimer = 0
    delayed_slope = 0

    while not collection_complete:
        try:
            time = 0
            #print ('Collecting Data...')

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
                updatePlot(time)

                # Update the time variable with the new time for the next data point
                time = time+time_between_readings_in_seconds

                window.update()

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




def updatePlot(time):
    #general wave
    #Using pyplot
    ax.plot(sensor_times,sensor_readings, color='k',label=column_headers[0])

    plt.ylabel(column_headers_string) #name and units of the sensor selected#
    plt.xlabel('Time(s)')
    plt.axis([sensor_times[0] - 2, sensor_times[-1] + 7, 0, 24])
    plt.grid(False) #This controls whether there is a grid on the graph
    plt.pause (0.05) # display the graph briefly, as the readings are taken

    #prevoice lines

    #voice bar


class FluencyTrainer(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Beau's Fluency Trainer")


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, RunningPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="start page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Start", command=lambda: controller.show_frame(RunningPage))
        button1.pack()

class RunningPage(tk.Frame):
    def __init__(self, parent, controller):

        global time_between_readings_in_seconds
        global number_of_readings
        global digits_of_precision
        global period_in_ms

        global column_headers
        global column_headers_string

        global sensor_times
        global sensor_readings

        #data collection
        global collection_complete
        global removeData
        global pvPause

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="running page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        #time.sleep(5)
        #updatePlot(self)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)





        while not collection_complete:
            try:
                time = 0
                #print ('Collecting Data...')

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
                    updatePlot(time)

                    # Update the time variable with the new time for the next data point
                    time = time+time_between_readings_in_seconds

                    Frame.update()

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







app = FluencyTrainer()

#th = Thread(target=collectAndPlot, , args=(self))
#th.daemon = True #tells the thread to quit if the GUI (master thread) quits.
#th.start()

app.geometry("1280x720")
#ani = animation.FuncAnimation(fig, updatePlot, 5)
#ani = animation.FuncAnimation(fig, animate, interval=250, blit=False)
app.mainloop()
