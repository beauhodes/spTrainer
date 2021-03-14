#By Beau Hodes
#Speech sensor, CAFET based

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import time
import random
from tkinter import *
from gdx import gdx
import pyaudio
import wave
import audioop
from collections import deque
import matplotlib.pyplot as plt
import platform, multiprocessing


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

    global line,ax,canvas
    global xs
    xs = []
    global ys
    ys= []
    global pvWait
    pvWait = 0
    global baseLine
    baseLine = 0
    global maxLine
    maxLine = 23
    global pvThreshold
    pvThreshold = maxLine * .8
    global peakWidth
    peakWidth = .7
    global peakWidthPv
    peakWidthPv = peakWidth + .1

    fig, ax = plt.subplots(1,1,figsize=(10,10))
    plt.ylabel("Force(N)")
    plt.xlabel('Time(s)')
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
    ax.set_ylim([baseLine,maxLine])


def prevoice(ys):
    global pvWait
    global xs
    global pvThreshold
    global peakWidth
    if(ys[-1] > ys[-3] and pvWait > 5 and ys[-1] > pvThreshold): #exhale found
        print("found it")
        ax.plot([xs[-1] + peakWidth, xs[-1] + peakWidth], [0, 24], 'k-', lw=1)
        ax.plot([xs[-1] + peakWidthPv, xs[-1] + peakWidthPv], [0, 24], 'k-', lw=1)
        pvWait = 0
    else:
        pvWait += 1



def updateplot(q):
    global pvWait
    try:       #Try to check if there is data in the queue
        result=q.get(block=True)
        if(result != 'empty'):
            print (result)

            if result[0] !='Q':
                xs.append(result[0])
                ys.append(result[1])
                if(result[0] > 5):
                    line = ax.plot(xs[-10:], ys[-10:], color='k', label="hi")
                    ax.set_xlim([xs[-20],xs[-1]+3])
                    prevoice(ys)
                else:
                    line = ax.plot(xs,ys, color='k',label="hi")
                    ax.set_xlim([xs[0],xs[-1]+3])

                canvas.draw()
                window.after(100,updateplot,q)

            else:
                 print ('done')
                 exit()

    except Exception as e:
        print(e)
        window.after(5,updateplot,q)


def simulation(q):

    import time
    from gdx import gdx #The gdx function calls are from a gdx.py file inside the gdx folder, which must be with this program.

    gdx = gdx.gdx()

    time_between_readings_in_seconds = 0.2
    number_of_readings = 500
    digits_of_precision = 2

    gdx.open_usb()
    gdx.select_sensors([1]) # You will be asked to select the sensors to be used. You can select up to three.

    sensor_times=[]
    sensor_readings=[]
    period_in_ms = time_between_readings_in_seconds*1000

    gdx.start(period_in_ms)

    # Data Collection:

    collection_complete=False
    while not collection_complete:
        try:
            time = 0
            print ('Starting...')

            for i in range(0,number_of_readings):

                # This is where we are reading the list of measurements from the sensors.
                measurements=gdx.read()
                if measurements == None:
                    break

                q.put([time, measurements[0]])

                # Update the time variable with the new time for the next data point
                time = time+time_between_readings_in_seconds

            # The data collection loop is finished
            collection_complete=True
            print ('Data collection complete.')

            #stop sensor readings and disconnect device
            gdx.stop()
            gdx.close()

            q.put('Q')
            exit()


        except KeyboardInterrupt:
            collection_complete=True
            gdx.stop() #Stop sensor readings
            gdx.close()#Disconnect the device
            print ('data  collection stopped by keypress')
            print ('Number of readings: ',i+1)
            q.put('Q')
            exit()








    # iterations = [x for x in range(1,50)]
    # for i in iterations:
    #     q.put([random.randint(1,10), i])
    #     # if not i % 10:
    #     #     time.sleep(.01)
    #     #         #here send any data you want to send to the other process, can be any pickable object
    #     #     q.put([random.randint(1,10), i])
    # q.put('Q')
    # exit()

if __name__ == '__main__':
    if platform.system() == "Darwin":
        multiprocessing.set_start_method('spawn')
        main()
