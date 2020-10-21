#By Beau Hodes
#Speech sensor, CAFET based

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
#----------------------------------------------------------------------------

#---------------------------sensor setup-------------------------------------
#gdx = gdx.gdx()
#gdx.open_usb()
#gdx.select_sensors([1])
#----------------------------------------------------------------------------

#---------------------------microphone setup---------------------------------

#----------------------------------------------------------------------------

#----------------------------variable setup---------------------------------
fig, ax = plt.subplots()
testArr = [0,1,2,3,4,5,6,7,8,9,10]
testVals = [13,8,7,6,5,4,6,7,8,9,12]

def carry_on():
    global testArr
    global testVals
    x=13
    y = 11
    for i in range (1,50):
        testArr.append(y)
        testVals.append(x)
        x = x + 1
        y = y + 1
        time.sleep(4)
        #plot_graph()

def plot_graph():
    global testArr
    global testVals
    #Using pyplot
    ax.plot(testArr,testVals, color='r',label="labeltest")

    plt.ylabel("ylabletest") #name and units of the sensor selected
    plt.xlabel('Time(s)')
    #plt.axis([sensor_times[0] - 2, sensor_times[-1] + 7, 0, 24])
    plt.axis([testArr[0] - 2, testArr[-1] + 3, 0, 24])
    plt.grid(False) #This controls whether there is a grid on the graph
    #plt.pause (0.05) # display the graph briefly, as the readings are taken
    time.sleep(2)
    print(testArr)

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
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="running page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        #button1 = ttk.Button(self, text="Home", command=lambda: controller.show_frame(StartPage))
        button1 = ttk.Button(self, text="Home", command=lambda: plot_graph())
        button1.pack()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        plot_graph()
        #time.sleep(2)
        #


        def makeThread(self):
            return
            # th = Thread(target=carry_on())
            # th.daemon = True # this line tells the thread to quit if the GUI (master thread) quits.
            # th.start()
            # tk.Frame.update(self)


    def collectData(self):
        global measurements

        measurements = gdx.read()


th = Thread(target=carry_on())
th.daemon = True # this line tells the thread to quit if the GUI (master thread) quits.
th.start()
app = FluencyTrainer()
app.geometry("1280x720")
#ani = animation.FuncAnimation(fig, updatePlot, 5)
app.mainloop()

if __name__ == '__main__':

    app = FluencyTrainer()
    leftFrame = Frame(root)
    leftFrame.pack(side=LEFT)
    rightFrame = Frame(root)
    rightFrame.pack(side=RIGHT)
    playButton = Button(leftFrame, text="Play", fg="blue",
        command= lambda: Threader(name='Play-Thread'))
    stopButton = Button(rightFrame, text="Stop", fg="red",
        command= lambda: Threader(name='Stop-Thread'))
    playButton.pack(side=TOP)
    stopButton.pack(side=BOTTOM)
    root.mainloop()
