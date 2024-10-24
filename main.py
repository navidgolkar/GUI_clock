# Author: Yasaman Hosseini
# Description: This file contains a GUI clock and timer functionalities.
# It creates a window with a clock displaying current time, day, and date,
# along with the ability to set a countdown timer and start/stop a timer,
# and save timer records to a chosen file.

import tkinter as tk
import time
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime

# GUI setup
root = tk.Tk()
root.geometry("500x500")
root.title("GUI Clock")
root.configure(background='violet')


# Function to update the clock display
def change_clock():
    current_time = time.localtime()
    time_string = time.strftime("%H:%M:%S", current_time)
    day_string = time.strftime("%A", current_time)
    date_string = time.strftime("%b %d, %Y", current_time)

    time_label.config(text=time_string)
    day_label.config(text=day_string)
    date_label.config(text=date_string)

    time_label.after(1000, change_clock)


# Clock labels
time_label = tk.Label(root, font=("8514oem", 48), fg="white", bg="black")
time_label.grid(row = 0, column = 0, columnspan = 3, sticky = tk.S)

day_label = tk.Label(root, font=("8514oem", 24), fg="white", bg="black")
day_label.grid(row = 1, column = 0, columnspan = 3)

date_label = tk.Label(root, font=("8514oem", 24), fg="white", bg="black")
date_label.grid(row = 2, column = 0, columnspan = 3, sticky = tk.N)

# Countdown timer setup
hourString = tk.StringVar()
minuteString = tk.StringVar()
secondString = tk.StringVar()

hourString.set("00")
minuteString.set("00")
secondString.set("00")

hourTextbox = tk.Entry(root, width=3, font=("8514oem", 25, ""), textvariable=hourString)
minuteTextbox = tk.Entry(root, width=3, font=("8514oem", 25, ""), textvariable=minuteString)
secondTextbox = tk.Entry(root, width=3, font=("8514oem", 25, ""), textvariable=secondString)


def runCountdown():
    global clockTime
    try:
        clockTime = int(hourString.get()) * 3600 + int(minuteString.get()) * 60 + int(secondString.get())
    except:
        print("Incorrect values")

    while clockTime > -1:

        totalMinutes, totalSeconds = divmod(clockTime, 60)

        totalHours = 0
        if totalMinutes > 60:
            totalHours, totalMinutes = divmod(totalMinutes, 60)

        hourString.set("{0:2d}".format(totalHours))
        minuteString.set("{0:2d}".format(totalMinutes))
        secondString.set("{0:2d}".format(totalSeconds))

        root.update()

        if clockTime == 0:
            messagebox.showinfo("", "Your countdown has ended!")
        else:
            time.sleep(1)

        clockTime -= 1


# Button to set countdown time
setCountdownButton = tk.Button(root, text='Set Time', bd='5', command=runCountdown)
setCountdownButton.grid(row = 3, column = 0, columnspan = 3, sticky = tk.S)

# Timer setup
timer_file = "timer.txt"

timer_running = False
start_time = None
run_time = 0

# Function to start or stop the timer
def start_stop_timer():
    global timer_running, start_time, run_time
    if not timer_running:
        start_time = datetime.now()
        timer_button.config(text="Stop Timer", bd='5')
        timer_running = True
        run_time = 0
        update_timer()
    else:
        end_time = datetime.now()
        duration = end_time - start_time
        write_to_file(start_time, end_time, duration)
        timer_button.config(text="Start Timer")
        timer_running = False

# Function to write timer records to a file
def write_to_file(start_time, end_time, duration):
    with open(file_entry.get(), "a") as file:
        file.write(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Duration: {duration}\n\n")


# Function to choose the file to save timer records
def choose_file():
    global timer_file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        timer_file = file_path

# Timer widgets
hourTextbox.grid(row = 4, column = 0, padx = 1, sticky = tk.NE)
minuteTextbox.grid(row = 4, column = 1, padx = 1, sticky = tk.N)
secondTextbox.grid(row = 4, column = 2, padx = 1, sticky = tk.NW)

timer_button = tk.Button(text="Start timer", command=start_stop_timer)
timer_button.grid(row = 5, column = 0, columnspan = 3, sticky = tk.S)

timer_label = tk.Label(root, font=("Arial", 20, "bold"), text="00:00:00")
timer_label.grid(row = 6, column = 0, columnspan = 3, sticky = tk.N)

file_label = tk.Label(text="Timer file:")
file_label.grid(row = 7, column = 0, columnspan = 3, sticky = tk.S)

file_entry = tk.Entry()
file_entry.insert(0, timer_file)
file_entry.grid(row = 8, column = 0, columnspan = 3)

file_button = tk.Button(text="Choose file", command=choose_file)
file_button.grid(row = 9, column = 0, columnspan = 3, sticky = tk.N)

# Function to update timer display
def update_timer():
    global run_time, timer_running
    if timer_running:
        run_time += 1
        minutes = int(run_time / 60)
        seconds = run_time % 60
        hours = int(minutes / 60)
        minutes = minutes % 60
        timer_label.config(text="{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds))
        root.after(1000, update_timer)

root.columnconfigure((0, 2), weight = 1);
for i in range(9):
    root.rowconfigure(i, weight = 1);
# Start the clock and timer
change_clock()
root.mainloop()
