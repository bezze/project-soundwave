import wave, struct
import math as m
from notes_full import *
from song import *


def open_wave(name,mode):

    sampleRate = 44100.0 # hertz
    duration = 10.0       # seconds
    frequency = 440.0    # hertz
    sampleWidth = 4
    maxVolume = 2**(8*sampleWidth-1) - 1

    wavef = wave.open(name,mode)
    wavef.setnchannels(1) # mono
    wavef.setsampwidth(sampleWidth)
    wavef.setframerate(sampleRate)

    return wavef

def close_wave(wavef):
    wavef.writeframes(b'')
    wavef.close()

# 2**15 = 32768
pi2 = 2*m.pi

def oscillator (f, vol, srate, length):
    w = [ int(vol*m.cos(f*2*m.pi*i/srate))  for i in  range(int(length * srate)) ]
    return w

def oscillator_damp (f, vol, damp, srate, length):
    w = []
    for i in  range(int(length * srate)):
        t = i/srate
        w.append( int(m.exp(-t/damp)*vol*m.cos(f*2*m.pi*t)) )
    return w

def compile(*args):
    W = [0]*len(args[0])
    for frame in range(len(W)):
        Frame = 0
        for w in args:
            Frame += w[frame]
        W[frame] = int(Frame/len(args))
    return W

def composer(wfile, nota, vol, lphi = 0, length = 1, lw=0, lwd=1):

    srate = wfile.getframerate()
    frq = note[nota] #[ note[i] for i in nota ]

    if type(frq) == list and type(vol) != list :
        vol = len(frq)*[vol]
    W = [];
    if type(frq) == list:
        for i in  range(int(length * srate)):
            w = 0
            for f,v in zip(frq,vol):
                w += int(v*m.cos(f*pi2*i/srate))
            w = int(w/len(frq))
            W.append( w )
            #lphi = m.arccos(w)
            data = struct.pack('<i', w )
            wfile.writeframesraw( data )
    else:
        sg=m.copysign(1,lwd)
        lphi = m.acos(lw/vol); 
        print(sg, m.copysign(1,m.sin(lphi)))
        if sg*m.sin(lphi) < 0:
            lphi = pi2 - lphi
            print("changing angle")
            print(sg, m.copysign(1,m.sin(lphi)))

        for i in range(int(length * srate)):

            w = int( vol*m.cos(frq*pi2*i/srate + lphi) ) 
            W.append( w )
            data = struct.pack('<i', w )
            wfile.writeframesraw( data )

        last_diff = vol*( m.sin(frq*pi2*i/srate + lphi)  - m.sin(frq*pi2*(i-1)/srate + lphi) )
        last = w

    return last, last_diff

    #wavef.writeframesraw( struct.pack('<i',  ) )



def write_notes(time,damp,**fvlist):
    raw_sound = []
    if type(fvlist["frq"]) == list:
        for freq,vol in zip(fvlist["frq"],fvlist["vol"]):
            #raw_sound.append(oscillator(freq, vol, sampleRate, time))
            raw_sound.append(oscillator_damp (f, vol, damp, srate, length))
        sound = compile(*raw_sound)
    else:
        #sound = oscillator(fvlist["frq"],fvlist["vol"], sampleRate, time)
        sound = oscillator_damp(fvlist["frq"],fvlist["vol"],damp, sampleRate, time)


    for i in range(int(time * sampleRate)):
        data = struct.pack('<i', sound[i])
        wfile.writeframesraw( data )
"""
"""

w_fi = open_wave('himno_fi_2.wav','w')
sampleWidth = w_fi.getsampwidth()
maxVolume = 2**(8*sampleWidth-1) - 1

last = 0;
last_d = 1;

for n,t in himno:
    last, last_d = composer(w_fi,n,maxVolume, length=t, lw=last,lwd=last_d)
close_wave(w_fi)

#w_not_fi = open_wave('himno_not_fi_2.wav','w')
#for n,t in himno:
#    last, last_d = composer(w_not_fi,n,maxVolume, length=t)
#close_wave(w_not_fi)

#fi = composer(note["G3"], maxVolume, length=4)
#fi = composer(note["D4"], maxVolume, length=4, lphi=fi)
#composer(note["G3"], maxVolume, length=4, lphi=fi)

#composer(note["G3"], maxVolume, length=4)
#composer(note["D4"], maxVolume, length=4)
#composer(note["G3"], maxVolume, length=4)

#write_notes(5,.2,frq=note["G3"], vol=maxVolume)



