import sys
import re
import os
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from array import array
import math
import pylab as pl
import matplotlib
import time 
import scipy.io as sio
from matplotlib import ticker
from matplotlib import pyplot as plt
from SCurveNP_8hits_addDecode import *
#filename='20180525_164333.dat.1'
t0=time.time()
t1=time.time()
print("start decoding frames!",t1-t0)
filename='/u1/atlas-chess2-Asic-tests/data/data_h/SpeedStreamReadoutTest/Streamreadout_Speed_05252018_payloadsize_0x7_20000Hz.dat.1'

numberOfFrames=0
alldata=frame_data()
allFrame=[]
frame_header=[0]
file_o=open(filename,mode='rb')
file_finished=1
time_all=[]
while(file_finished):
#while file_header=get_frame_header(file_o):
    file_header=get_frame_header(file_o)
    if len(file_header)==0:
        file_finished=0
        #print("finish reading from the file")
        break
   # print("########################################################")
   # print("The index of this frame: ",numberOfFrames)
   # print("first 32 bits : ",bin(file_header[0])[2:].rjust(32,"0"))
   # print("second 32 bits : ",bin(file_header[1])[2:].rjust(32,"0"))
    frame_Size = int(file_header[0]/2)-2 #file_header[0]: frame size in bytes, including 4 bytes from the header
  #  print ("size of this frame: ",frame_Size)
  #  print("########################################################")
    frame_rawData,frame_rawHeader,frame_all,time_stamp=get_frame(file_o,frame_Size,0)
    time_all.append(time_stamp)
    numberOfFrames+=1
    allFrame.append(frame_all)

#for i in range(len(time_all)-1):
#    print("time different : ",(time_all[i+1]-time_all[i]))
    #print("time different : ",(time_all[i+1]-time_all[i])*(1/320000000))
t2=time.time()
print("finish decoding :",t2-t1)
for index in range(len(allFrame)):
    frame_data=allFrame[index][16:].copy()
    for i in range(len(frame_data)):
        alldata.add_data("buffer",frame_data[i],i)


if 1:
    #plt.ion()
    t3=time.time()
    print("start plotting",t3-t2)
    figure_0,ax=plt.subplots(figsize=(11,9))
    
    ax.set_axis_off()
    chass2_point=[(87.9,108),(20228,108),(24300,108),(24300,18517),(24300,18517),(20227,18517),(87.9,18517),(87.9,13413),(87.9,13138),(87.9,8034),(87.9,5212),(20227,5212),(20227,8034),(20227,13138),(20227,13413)]
    for i in range(9):
        ax.plot([chass2_point[i][0],chass2_point[i+1][0]],[chass2_point[i][1],chass2_point[i+1][1]],'k')
    ax.plot([chass2_point[0][0],chass2_point[9][0]],[chass2_point[0][1],chass2_point[9][1]],'k')
    ax.plot([chass2_point[1][0],chass2_point[5][0]],[chass2_point[1][1],chass2_point[5][1]],'k')
    for i in range(7,12,1):
        ax.plot([chass2_point[i][0],chass2_point[21-i][0]],[chass2_point[i][1],chass2_point[21-i][1]],'k')
    for i in range(len(alldata.hitmap_t2)):
        for j in range(0,13):
            alldata.hitmap_t2[i][j]=0
            alldata.hitmap_t1[i][j]=0
            alldata.hitmap_t0[i][j]=0
    l_size=10
    pl.figure(1)
    ax0=figure_0.add_axes([0.16,0.144,0.586,0.1955])
    ax0.clear()
    plt.imshow(alldata.hitmap_t2,aspect="auto",cmap='gray',origin='upper',vmin=0,interpolation='nearest')
    ax1=figure_0.add_axes([0.16,0.4445,0.586,0.1955])
    ax1.clear()
    plt.imshow(alldata.hitmap_t1,aspect="auto",cmap='gray',origin='upper',vmin=0,interpolation='nearest')
    ax2=figure_0.add_axes([0.16,0.6485,0.586,0.1955])
    ax2.clear()
    plt.imshow(alldata.hitmap_t0,aspect="auto",cmap='gray',origin='lower',vmin=0,interpolation='nearest')
    t4=time.time()
    print("finish plotting",t4-t3)
    plt.show()
   # figure_0.canvas.draw()
   # figure_0.canvas.flush_events()

