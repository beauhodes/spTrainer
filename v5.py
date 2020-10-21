#By Beau Hodes
#Speech sensor, CAFET based

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import multiprocessing
import time
import random
from tkinter import *


#Create a window
window=Tk()



def main():
    #Create a queue to share data between process
    q = multiprocessing.Queue()

    #allow device monitoring in other process
    simulate=multiprocessing.Process(None,simulation,args=(q,))
    simulate.start()

    #Create the base plot
    plot()

    #Call a function to update the plot when there is new data
    updateplot(q)

    window.mainloop()
    print ('Done')


def plot():    #Function to create the base plot, make sure to make global the lines, axes, canvas and any part that you would want to update later

    #TEMPORARY
    fig, ax = plt.subplots()
    #END TEMPORARY

    global line,ax,canvas
    global times, readings
    times = []
    readings = []
    fig, ax = plt.subplots(1,1,figsize=(10,10))
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
    #line, = ax.plot(sensor_times,sensor_readings, color='k',label=column_headers[0])




def updateplot(q):

    #TEMPORARY
    #HERE IS PLOT FROM FIRST
    #Using pyplot
    ax.plot(sensor_times,sensor_readings, color='k',label=column_headers[0])

    plt.ylabel(column_headers_string) #name and units of the sensor selected#
    plt.xlabel('Time(s)')
    plt.axis([sensor_times[0] - 2, sensor_times[-1] + 7, 0, 24])
    plt.grid(False) #This controls whether there is a grid on the graph
    plt.pause (0.05) # display the graph briefly, as the readings are taken
    #END TEMPORARY



    try:       #Try to check if there is data in the queue
        result=q.get_nowait()
        times.append(result[0])
        readings.append(result[0])

        if (result != "Q"):
             print (result)
                 #here get crazy with the plotting, you have access to all the global variables that you defined in the plot function, and have the data that the simulation sent.
             line = ax.plot(times,readings, color='k',label="hi")
             canvas.draw()
             window.after(50,updateplot,q)

             #do removal of data if needed, find out how much to remove

        else:
             print ('done')
    except:
        print ("empty")
        window.after(50,updateplot,q)


def simulation(q):

    #------------------------------SET UP---------------------------------------------
    gdx = gdx.gdx()

    time_between_readings_in_seconds = 0.1
    number_of_readings = 200
    digits_of_precision = 2

    period_in_ms = time_between_readings_in_seconds*1000

    gdx.open_usb()
    gdx.select_sensors([1])

    sensor_times=[]
    sensor_readings=[]
    print_table_string = []
    #---------------------------------END SETUP----------------------------------------

    #------------------------------DATA COLLECTION-------------------------------------
    gdx.start(period_in_ms)
    collection_complete = False
    newMeasurements = None
    newTimes = None
    removeData = False
    #pvPause = True
    #isRising = False
    #pauseTimer = 0
    #delayed_slope = 0
    while not collection_complete:
        try:
            time = 0
            print ('Collecting Data...')

            # Print the column headers in terminal
            print('Time(s), Reading(s)')

            for i in range(0,number_of_readings):

                #TEMPORARY/POSSIBLY
                newMeasurements = None
                newTimes = None
                #END TEMPORARY/POSSIBLY

                # Create a list of times to be used in the graph and data table
                newTimes.append(time)
                #if(time > 3):
                    #newTimes.pop(0)
                    #removeData = True

                # Read the list of measurements from the sensor
                measurements = gdx.read()
                if measurements == None:
                    break

                # Store each sensor's measurement in a list to be used in plot_graph() and print_table()
                data_string = ''
                for data in measurements:
                    newMeasurements.append(data)
                    #if(removeData == True):
                        #newMeasurements.pop(0)
                        #delayed_slope = (sensor_readings[-1] - sensor_readings[-3]) / (sensor_times[-1] - sensor_times[-3])#y2-y1 / x2-x1
                        #print('cur slope: ', delayed_slope)

                    # Build a string for printing to the terminal
                    round_data = str(round(data,digits_of_precision))
                    data_string = data_string + round_data + '   '

                # Print the time and the data to the terminal
                print(str(round(time,2)) + '   '+ data_string)

                # If the last reading is finished update the graph's title
                if  i >=number_of_readings-1:
                    plt.title('Reading(s) vs Time(s)')

                # Call the plot_graph() function to update the graph with the new data set.
                q.put([newTimes, newMeasurements])

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
            q.put("Q")


        except KeyboardInterrupt:
            collection_complete=True
            gdx.stop() #stop sensor readings
            gdx.close()#disconnect the device
            stream.close() #stop voice stream
            p.terminate() #terminate pyaudio object
            print ('data  collection stopped by keypress')
            print ('Number of readings: ',i+1)
    #---------------------------------END DATA COLLECTION------------------------------

if __name__ == '__main__':
    main()
