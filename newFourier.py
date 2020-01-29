import librosa

#Thank you to Sanket Doshi for his Music Feature Extraction in Python

def do_the_thing_2(filename):
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
	thresh = 0
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

print(do_the_thing_2('300Hz.wav'))
