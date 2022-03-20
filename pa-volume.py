import tkinter as tk
from tkinter import *
import os
from subprocess import PIPE, run

# Allows you to adjust your volume beyond 100% easily
# wraps the following commands
# pacmd list-sinks
# pactl set-sink-volume 0 200%

window = tk.Tk()
window.title('Volume Control')
window.minsize(width=400,height=200)
volume = DoubleVar()
devices = {}

def command(commands):
    result = run(commands, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result.stdout

def getSinks():
    output = command(['pacmd','list-sinks'])
    data = output.replace('\t','')
    data = data.replace('* index:','index:')
    return data

def getDevices():
    #get the sinks, probably could use https://pypi.org/project/pulsectl/#installation
    devices.clear()
    data = getSinks()
    currentIndex = ''

    for line in data.split('\n'):
        li = line.strip()
        if li.startswith('index: '):
            currentIndex = li.replace('index: ', '')
        
        if li.startswith('device.description ='):
            pos = len('device.description = ')
            tmp = li[pos:len(li)]
            key = tmp.replace('"','')
            devices[key] = currentIndex

def volumeChanged(self):
    strVolume = str(int(volume.get()))
    lbDevices = window.children['lbDevices']
    selected = lbDevices.curselection()[0]
    key = lbDevices.get(selected)
    sink = devices[key]
    cmd = 'pactl set-sink-volume ' + sink + ' ' + strVolume + '%'
    os.system(cmd)

def itemChanged(event):
    #get the volume of the current sink
    selected = event.widget.curselection()[0]
    key = event.widget.get(selected)
    data = getSinks()
    currentIndex = ''

    for line in data.split('\n'):
        li = line.strip()
        if li.startswith('index: '):
            currentIndex = li.replace('index: ', '')
        if li.startswith('volume: ') and currentIndex == devices[key]:
            values = li.split('/')
            value = int(values[1].replace('%','').strip())
            scVolume = window.children['scVolume']
            scVolume.set(value)
            return

def updateDevices(lb):
    lb.delete(0,END)
    for key in devices:
        lb.insert(END, key)

def main():
    getDevices()
    volume.set(0)
    Grid.rowconfigure(window, 0,weight=1)
    Grid.columnconfigure(window,0,weight=1)
    lbDevices = Listbox(window,name='lbDevices')
    lbDevices.bind("<<ListboxSelect>>", itemChanged)
    scVolume = Scale(window, from_ = 0, to = 200,orient = HORIZONTAL,variable=volume,command=volumeChanged,name='scVolume')
    lbDevices.grid(row=0, column=0, sticky= "nsew")
    scVolume.grid(row=1, column=0, sticky= "nsew")

    updateDevices(lbDevices)
    if lbDevices.size() > 0:
        lbDevices.select_set(0)
        lbDevices.activate(0)
        e = Event()
        e.widget = lbDevices
        itemChanged(e)

    window.mainloop()

if __name__:
    main()