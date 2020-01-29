import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import numpy as np
import math

def get_note(rawdata): #take fourier transform
    c = fft(rawdata)
    note = (abs(c).tolist().index(max(abs(c).tolist())))/3
    note = round(note, 1)
    return note


def get_time(seperated_note, fs): #determines how long note was
    time_in_sec = len(seperated_note)/fs
    time_in_sec = round(time_in_sec, 3)
    return(time_in_sec)

def seperate_notes(whole_recording, threshold, fs): 
    seperated_notes=[]
    freq_and_time = []
    j = 0
    count = 0
    for i in range(int(len(whole_recording)/441)):
        #print(str(len(whole_recording)) + ' ' + str(i*10 +100))
        if abs(whole_recording[i*441]) < threshold:
            count = count + 1
        else:
            if count > 10:
                # parce previous note and adds to freq/time array
                #print(j)
                #print((i+math.floor(count/2))*10)
                single_note = whole_recording[j:(i+math.floor(count/2))*441]
                freq_and_time.append([get_note(single_note), get_time(single_note,fs)])
                j = int((i - count/2)*441)
            count = 0

    single_note = whole_recording[j:(i+math.floor(count/2))*441]
    freq_and_time.append([get_note(single_note), get_time(single_note,fs)])
    j = (i - count/2)*441
    return(freq_and_time)

def do_the_thing(filename):
    fs, data = wavfile.read(filename) # load the data
   # data = data.T[0]  #ONLY FOR MACS
    data = [(ele/2**8.)*2-1 for ele in data]
    freq_and_time = seperate_notes(data, (sum(map(abs,data))/len(data)), fs)
    #print(sum(abs(data))/len(data))
    #print(freq_and_time)
    #print(len(freq_and_time))
    return(freq_and_time)
