#By Beau Hodes
#Speech sensor, CAFET based

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import multiprocessing
import time
import random
from tkinter import *
from gdx import gdx
import pyaudio
import wave
import audioop
from collections import deque
import matplotlib.pyplot as plt


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
    #fig = matplotlib.figure.Figure()
    #ax = fig.add_subplot(1,1,1)
    fig, ax = plt.subplots(1,1,figsize=(10,10))
    plt.ylabel("ylabletest") #name and units of the sensor selected
    plt.xlabel('Time(s)')
    #ax.xlabel('Time(s)')
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
    #line, = ax.plot([1,2,3], [1,2,10])




def updateplot(q):
    try:       #Try to check if there is data in the queue
        result=q.get_nowait()
        print (result)

        if result[0] !='Q':
            xs.append(result[1])
            ys.append(result[0])
            line = ax.plot(xs,ys, color='k',label="hi")
            canvas.draw()
            window.after(50,updateplot,q)
             #print (result)
                 #here get crazy with the plotting, you have access to all the global variables that you defined in the plot function, and have the data that the simulation sent.
             # line.set_ydata([1,result[0],10])
             # ax.draw_artist(line)
             # canvas.draw()
             # window.after(50,updateplot,q)


             #TEMPORARY
             #HERE IS PLOT FROM FIRST
             #Using pyplot
             #ax.plot(result[1],result[0], color='k',label=column_headers[0])
             #line, = ax.plot(xs,ys)
             #line = ax.plot(xs,ys, color='k',label="hi")
             #set the axis
             #line.set_data([result[1],result[0],10])

             #plt.axis([sensor_times[0] - 2, sensor_times[-1] + 7, 0, 24])
             #canvas.draw()
             #window.after(50,updateplot,q)
             #END TEMPORARY
        else:
             print ('done')
    except:
        print ("empty")
        window.after(20,updateplot,q)


def simulation(q):
    iterations = [x for x in range(1,100)]
    for i in iterations:
        q.put([random.randint(1,10), i])
        # if not i % 10:
        #     time.sleep(.01)
        #         #here send any data you want to send to the other process, can be any pickable object
        #     q.put([random.randint(1,10), i])
    q.put('Q')

if __name__ == '__main__':
    main()
