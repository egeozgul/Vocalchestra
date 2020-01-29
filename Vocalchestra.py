#Huge credit and thanks to the python-sounddevice documentation page for 
#showing us how to use their library and record to .wav files
#https://python-sounddevice.readthedocs.io/en/0.3.14/index.html
#NEW RECORD WITH TIMER BC WE CAN'T FIGURE OUT THREADS :)
from tkinter import *
#from tkinter.ttk import Combobox
from tkinter import ttk
from playsound import playsound
from pydub import AudioSegment
#from pydub.playback import play
import argparse
import tempfile
import queue
import sys
from tkinter import *
import pyaudio as pyaudio

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
#assert numpy  # avoid "imported but unused" message (W0611)
from timeit import default_timer as time
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import numpy as np
import math
import librosa
import math
import numpy as np


global countTracks
countTracks = -1

#BASE            = 392       #sample file note is g4
#
#PATH            = ''
#
#VIOLIN          = 'violin'
#VIOLIN_INDEX    = 0
#
#CELLO           = 'cello'
#CELLO_INDEX     = 1
#
#FLUTE           = 'flute'
#FLUTE_INDEX     = 2
#
#PIANO           = 'piano'
#PIANO_INDEX     = 3
#
#TRUMPET         = 'trumpet'
#TRUMPET_INDEX   = 4
#
#GUITAR          = 'guitar'
#GUITAR_INDEX    = 5
#
#def initializeInstruments():
#    instruments = [PATH] * 6
#
#    instruments[VIOLIN_INDEX]   += VIOLIN + '.wav'
#    instruments[CELLO_INDEX]    += CELLO + '.wav'
#    instruments[FLUTE_INDEX]    += FLUTE + '.wav'
#    instruments[PIANO_INDEX]    += PIANO + '.wav'
#    instruments[TRUMPET_INDEX]  += TRUMPET + '.wav'
#    instruments[GUITAR_INDEX]   += GUITAR + '.wav'
#
#    return instruments
#    
#def instrumentToIndex(instrument):
#    if instrument == VIOLIN:
#        return VIOLIN_INDEX
#    elif instrument == CELLO:
#        return CELLO_INDEX
#    elif instrument == FLUTE:
#        return FLUTE_INDEX
#    elif instrument == PIANO:
#        return PIANO_INDEX
#    elif instrument == TRUMPET:
#        return TRUMPET_INDEX
#    elif instrument == GUITAR:
#        return GUITAR_INDEX
#    
#def freqToStepsFromBase(freq):
#    if(freq == 0):
#        freq +=1
#    return int(round(12*math.log2(freq/BASE)))
#    
#def createNote(instrument, freq, duration):
#    instruments = initializeInstruments()
#    audio_file = instruments[instrumentToIndex(instrument)]
#    base_duration = librosa.get_duration(filename=audio_file)
#    duration_coefficient = base_duration / duration
#    steps = freqToStepsFromBase(freq)
#    if instrument == TRUMPET:
#        steps -= 12
#    elif instrument == CELLO:
#        steps -= 24
#
#    y, sr = librosa.load(audio_file)
#    y = librosa.effects.time_stretch(y, duration_coefficient)
#    y = librosa.effects.pitch_shift(y, sr,n_steps=steps)
#
#    note = [y, sr]
#    
#    return note
#
#trackListFiles = [];
#def combine(notes):
#    y = []
#    sr = notes[0][1]
#
#    for x in notes:
#        y = np.concatenate((y, x[0]))
#        
#    return [y, sr]
#
#def convert(notes_data, instrument):
#    notes = [] 
#    for x in notes_data:
#        notes.append(createNote(instrument, x[0], x[1]))
#
#    melody = combine(notes)
#    
#    #librosa.output.write_wav(PATH + instrument + '_new.wav', melody[0], melody[1])
#    sf.write(PATH + instrument + str(countTracks) + '.wav', melody[0], melody[1])
#    convertedTrack = PATH + instrument + str(countTracks) + '.wav'
#    trackListFiles.append(convertedTrack)
#
#


BASE            = 392       #sample file note is g4

PATH            = ''

VIOLIN          = 'violin'
VIOLIN_INDEX    = 0

CELLO           = 'cello'
CELLO_INDEX     = 1

FLUTE           = 'flute'
FLUTE_INDEX     = 2

PIANO           = 'piano'
PIANO_INDEX     = 3

TRUMPET         = 'trumpet'
TRUMPET_INDEX   = 4

GUITAR          = 'guitar'
GUITAR_INDEX    = 5

def initializeInstruments():
    instruments = [PATH] * 6

    instruments[VIOLIN_INDEX]   += VIOLIN + '.wav'
    instruments[CELLO_INDEX]    += CELLO + '.wav'
    instruments[FLUTE_INDEX]    += FLUTE + '.wav'
    instruments[PIANO_INDEX]    += PIANO + '.wav'
    instruments[TRUMPET_INDEX]  += TRUMPET + '.wav'
    instruments[GUITAR_INDEX]   += GUITAR + '.wav'

    return instruments
    
def instrumentToIndex(instrument):
    if instrument == VIOLIN:
        return VIOLIN_INDEX
    elif instrument == CELLO:
        return CELLO_INDEX
    elif instrument == FLUTE:
        return FLUTE_INDEX
    elif instrument == PIANO:
        return PIANO_INDEX
    elif instrument == TRUMPET:
        return TRUMPET_INDEX
    elif instrument == GUITAR:
        return GUITAR_INDEX
    
def freqToStepsFromBase(freq):
    if(freq == 0):
        freq +=1
    return int(round(12*math.log2(freq/BASE)))
    
def chord(y, sr):
    y2 = librosa.effects.pitch_shift(y, sr,n_steps=4)
    y3 = librosa.effects.pitch_shift(y, sr,n_steps=7)

    y = y + y2 + y3

    return y

def createNote(instrument, freq, duration):
    instruments = initializeInstruments()
    audio_file = instruments[instrumentToIndex(instrument)]
    base_duration = librosa.get_duration(filename=audio_file)
    duration_coefficient = base_duration / (duration+.01)
    if freq > 0:
        steps = freqToStepsFromBase(freq)
    else:
        steps = 0

    if instrument == TRUMPET:
        steps -= 12
    elif instrument == CELLO:
        steps -= 24
    elif instrument == GUITAR:
        steps -= 12

    y, sr = librosa.load(audio_file)
    y = librosa.effects.time_stretch(y, duration_coefficient)
    y = librosa.effects.pitch_shift(y, sr,n_steps=steps)

    if instrument == GUITAR:
        y = chord(y, sr) 

    if freq == 0:
        for x in y:
            x = 0

    note = [y, sr]
    
    return note

trackListFiles = [];
def combine(notes):
    y = []
    sr = notes[0][1]

    for x in notes:
        y = np.concatenate((y, x[0]))
        
    return [y, sr]

def convert(notes_data, instrument):
    notes = [] 
    for x in notes_data:
        notes.append(createNote(instrument, x[0], x[1]))

    melody = combine(notes)
    
    #librosa.output.write_wav(PATH + instrument + '_new.wav', melody[0], melody[1])
    sf.write(PATH + instrument + str(countTracks) + '.wav', melody[0], melody[1])
    convertedTrack = PATH + instrument + str(countTracks) + '.wav'
    trackListFiles.append(convertedTrack)










#--------------------------------------------------------------------------------------------------------
global nameOfFile;
nameOfFile = ""

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def getName():
    return nameOfFile


q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def runRecord():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        'filename', nargs='?', metavar='FILENAME',
        help='audio file to store recording to')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-r', '--samplerate', type=int, help='sampling rate')
    parser.add_argument(
        '-c', '--channels', type=int, default=1, help='number of input channels')
    parser.add_argument(
        '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
    args = parser.parse_args(remaining)
    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])
        if args.filename is None:
            args.filename = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                            suffix='.wav', dir='')
    
        # Make sure the file is opened before recording anything:
        with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                          channels=args.channels, subtype=args.subtype) as file:
            with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                channels=args.channels, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                start = time()
                while True:
                    file.write(q.get())
                    if time() >= start + duration.get():
                        break
    
    
            print('\nRecording finished: ' + repr(args.filename))
            global nameOfFile
            nameOfFile = args.filename

            print(nameOfFile)
            #parser.exit(1)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

#-------------------------------------------------------------------------------
#Start Fourier
#---------------------------------------------------------------------------------
#
# def get_note(rawdata): #take fourier transform
#     c = fft(rawdata)
#     note = (abs(c).tolist().index(max(abs(c).tolist())))/3
#     note = round(note, 1)
#     return note


# def get_time(seperated_note, fs): #determines how long note was
#     time_in_sec = len(seperated_note)/fs
#     time_in_sec = round(time_in_sec, 3)
#     return(time_in_sec)

# def seperate_notes(whole_recording, threshold, fs): 
#     seperated_notes=[]
#     freq_and_time = []
#     j = 0
#     count = 0
#     for i in range(int(len(whole_recording)/441)):
#         #print(str(len(whole_recording)) + ' ' + str(i*10 +100))
#         if abs(whole_recording[i*441]) < threshold:
#             count = count + 1
#         else:
#             if count > 10:
#                 # parce previous note and adds to freq/time array
#                 #print(j)
#                 #print((i+math.floor(count/2))*10)
#                 single_note = whole_recording[j:(i+math.floor(count/2))*441]
#                 freq_and_time.append([get_note(single_note), get_time(single_note,fs)])
#                 j = int((i - count/2)*441)
#             count = 0

#     single_note = whole_recording[j:(i+math.floor(count/2))*441]
#     freq_and_time.append([get_note(single_note), get_time(single_note,fs)])
#     j = (i - count/2)*441
#     return(freq_and_time)

# def do_the_thing(filename):
#     fs, data = wavfile.read(filename) # load the data
#    # data = data.T[0]  #ONLY FOR MACS
#     data = [(ele/2**8.)*2-1 for ele in data]
#     freq_and_time = seperate_notes(data, (sum(map(abs,data))/len(data)), fs)
#     #print(sum(abs(data))/len(data))
#     #print(freq_and_time)
#     #print(len(freq_and_time))
#     return(freq_and_time)







def do_the_thing(filename):
   x , sr = librosa.load(filename)
   #print(type(x), type(sr))

   X = librosa.stft(x)
   Xdb = librosa.amplitude_to_db(abs(X))
   #plt.figure(figsize=(14, 5))
   #librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz') 
   #If to pring log of frequencies  
   #librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
   #plt.colorbar()

   #print(len(Xdb))
   Xdbt = Xdb.transpose()
   #print(len(Xdbt))
   graph= []
   t = []
   thresh = -10
   for k in range(len(Xdbt)):
       Xdbtlist = Xdbt[k].tolist()
       note = Xdbtlist.index(max(Xdbtlist))*10.75
       if max(Xdbtlist) < thresh:
           note = 0
       graph.append(note)
       t.append(k/(130/3))
       
   freq_and_time = []
   tstart = 0
   count = 0
   restcount = 0

   #print(graph)
       
   for h in range(len(graph)):
       if(graph[h] != 0):
           if(count == 0):
               freq_and_time.append([0 , restcount*3/130])
               restcount = 0
               tstart = h
               count = count + 1
           else:
               count = count + 1
       elif(count!=0):
           freq_and_time.append([(sum(graph[tstart:tstart+count])/(count+.01)) , count*3/130])
           count  = 0
           rest_start = h
       else:
           restcount = restcount + 1
   freq_and_time.append([(sum(graph[tstart:tstart+count])/(count+.01)) , count*3/130])
           
           
   return(freq_and_time)

#print(do_the_thing_2('300Hz.wav'))

#---------------------------------------------------------------------------------------
trackList = [];
master = Tk()
#var1 = IntVar()

def record():
    print ("recording:)")
    print ("duration val: ",duration.get())
    Label(master, text="RECORDING").place(x=250, y=7)
    runRecord()
    print ("stop recording:)")
    Label(master, text="STOPPED     ").place(x=250, y=7)


def play():
    print ("playing")
    temp = nameOfFile
    print(temp)
    filename = temp
    # Extract data and sampling rate from file
    data, fs = sf.read(filename, dtype='float32')  
    sd.play(data, fs)
    
    for x in range (1,1):
        mixed = AudioSegment.from_file()



global fileName;
fileName = StringVar()
cList = []
def addTrack():
    global countTracks
    isUnique = True;
    for i in trackList:
        if(i == fileName.get()):
            isUnique = False
            break
    if(isUnique == True):
        countTracks += 1
        print("fileName:",fileName.get())
        var = IntVar()
        #trackListState.append(var)
        #c = Checkbutton(master, text=fileName.get(), variable = var).pack(side = TOP,anchor=W)
        Checkbutton(master, text=fileName.get(), variable = var, command = lambda: toggle()).pack(side = TOP,anchor=W)
        #cList.append(IntVar(master, value = c))
        trackList.append(fileName.get())
    elif(isUnique == False):
        print("same name")

def checkB(var, event):
    print(cList[var].get())
    

clickedValues = []
#def toggle():

    

def playProject():
    #for tracks in trackList:
    song1 = AudioSegment.from_file(trackListFiles[0])
    song2 = AudioSegment.from_file(trackListFiles[1])
    combine = song1.overlay(song2)
    for i in range(2, len(trackListFiles)):
        song = AudioSegment.from_file(trackListFiles[i])
        combine = combine.overlay(song)

    combine.export("combined.wav", format='wav')

    print("playProject")


def saveProject():
    print("saveProject")

def convertMusic():
    global comboExample

    if comboExample.get() == "violin":
        convert(do_the_thing(nameOfFile), 'violin')
         
    
    #^if user select prova show this message 
    elif comboExample.get() == "guitar":
        convert(do_the_thing(nameOfFile), 'guitar')
        #messagebox.showinfo("What user choose", "you choose ciao")
    
     #^if user select ciao show this message 
    elif comboExample.get() == "trumpet":
        convert(do_the_thing(nameOfFile), 'trumpet')
    
    elif comboExample.get() == "piano":
        convert(do_the_thing(nameOfFile), 'piano')
    
    elif comboExample.get() == "cello":
        convert(do_the_thing(nameOfFile), 'cello')

    elif comboExample.get() == "flute":
        convert(do_the_thing(nameOfFile), 'flute')

def callbackFunc(event):
     print("New Element Selected")




    


#data=("violin", "guitar","trumpet","piano", "cello", "flute")
frame = Frame(master, height=150, width=350)

global duration
duration = DoubleVar(master, value = 3)
Label(master, text="enter duration").place(x=5, y=5)
e = Entry(master, bd =5,textvariable = duration,width = 5).place(x=95, y=5)

Button(master,text='record',command=record).place(x=150, y=5)

#Combobox(master, values=data).place(x=5, y=37)
#global cmb;
#cmb = Combobox(master, width="20", values=["prova","ciao","come","stai"]).place(x=5, y=37)

global comboExample;
comboExample = ttk.Combobox(master, values=["violin", "guitar", "trumpet", "piano", "cello", "flute"])
comboExample.place(x=5, y=37)
#comboExample.bind("<<ComboboxSelected>>", callbackFunc)


Button(master,text='convert',command=convertMusic).place(x=155, y=35)
Button(master,text='play',command=play).place(x=210, y=35)


Label(master, text="file name").place(x=5, y=67)
Entry(master, bd =5,textvariable = fileName).place(x=65, y=65)
Button(master,text='add track',command=addTrack).place(x=195, y=65)
#addTrack()
#cList[0].checkB(0)





Button(master,text='play project',command=playProject).place(x=5, y=95)
Button(master,text='save project',command=saveProject).place(x=85, y=95)

frame.pack_propagate(0) # don't shrink
frame.pack()

master.mainloop()
