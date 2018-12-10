import numpy as np
import ctypes
import matplotlib #.pyplot as plt
import sys
import time
import re
import logging
import copy
import datetime
import json
import random
from matplotlib import pyplot as plt
#import matplotlib.animation as animation
from matplotlib.colors import LogNorm
from matplotlib import cm
from matplotlib import ticker
import scipy.io as sio
from threading import Timer

def StreamRO_concept(system,Run_number, nFrames, trigger_type, pixels, parameters_interested ,interested_range,save_path_name, file_l, hotpixel_m0, hotpixel_m1, hotpixel_m2, Trim):
    nColums = 32
    nRows   =128
    trim = Trim
    today1=time.strftime("%Y%m%d_%H%M%S",time.localtime())
    
    t1=time.time() 
    system.feb.Chess2Ctrl0.writeAllPixels(enable= 0,chargeInj= 1,trimI= trim)
    system.feb.Chess2Ctrl1.writeAllPixels(enable= 0,chargeInj= 1,trimI= trim)
    system.feb.Chess2Ctrl2.writeAllPixels(enable= 0,chargeInj= 1,trimI= trim)
    t2=time.time()
    print("Disable all pixels :"+str(t2-t1)+" s")
    
    t1=time.time() 
    pixels = pixels if (pixels!=None) else [ (row,col) for row in range(0,128,1) for col in range(0,32,1) ]
    for (row,col) in pixels:
        if ((row,col) not in hotpixel_m0):
            system.feb.Chess2Ctrl0.writePixel(enable = 1, chargeInj = 0, col=col, row=row, trimI=trim)   
        if ((row,col) not in hotpixel_m1):
            system.feb.Chess2Ctrl1.writePixel(enable = 1, chargeInj = 0, col=col, row=row, trimI=trim)   
        if ((row,col) not in hotpixel_m2):
            system.feb.Chess2Ctrl2.writePixel(enable = 1, chargeInj = 0, col=col, row=row, trimI=trim)   
    t2=time.time()
    print("enabling pixels interested :"+str(t2-t1)+" s")
    
    if len(trigger_type) == 2:
        for parameter in parameters_interested:
            save_fname=save_path_name+"StreamRO_softTrigger_Run"+Run_number+"_"+today1+"_"+str(parameter)
            StreamRO_SoftTrigger(system, nFrames, save_fname, parameter, interested_range, file_l, Trigger_r=trigger_type[1])
    else:
        for parameter in parameters_interested:
            save_fname=save_path_name+"StreamRO_externalTrigger_Run"+Run_number+"_"+today1+"_"+str(parameter)
            StreamRO_ExternalTrigger(system, nFrames, save_fname, parameter, interested_range, file_l)
    return save_fname

def StreamRO_SoftTrigger(system, nFrames, save_fname, parameter, interested_range, file_l, Trigger_r=1000):
    system.dataWriter.dataFile.set(save_fname+".dat")
    system.dataWriter._setOpen(system.dataWriter,system.dataWriter.open,True,1)
    file_l.write(save_fname+"\n")
    file_l.write("Changing "+parameter+": "+str(len(interested_range))+"\n")
    file_l.write("Taking "+str(nFrames)+ " frames per value\n")
    system.runControl.runRate.set(int(Trigger_r)) #set the trigger rate
    timer_repeat = nFrames/336

    process=0
    for i in interested_range:
        process+=1
        perc=process*100.0/len(interested_range)
        sys.stdout.write("%d"%perc)
        sys.stdout.write("%\r")
        sys.stdout.flush()
        eval(set_parameter(parameter,i))
        time.sleep(1.0)
        system.runControl.runState.set(1) #0 - 'Stopped'; 1 - 'Running'
        time.sleep(timer_repeat)
        #Timer_t=Timer(timer_repeat,system.runControl.runState.set(0))
        system.runControl.runState.set(0)
       # print("frame number: ",system.dataWriter._getFrameCount(system.dataWriter,system.dataWriter._getFrameCount))
        file_l.write(str(i)+"="+str(system.dataWriter._getFrameCount(system.dataWriter,system.dataWriter._getFrameCount))+" ")
        #Timer_t=Timer(timer_repeat,StreamRO_SoftTrigger_ReadingInTimer)
        #system.ReadAll()
    system.dataWriter._setOpen(system.dataWriter,system.dataWriter.open,False,1)
    sys.stdout.write("100%!\n")
    file_l.write("\n end of testing!") 
        

def StreamRO_ExternalTrigger(system, nFrames, save_fname, parameter, interested_range, file_l):     
    
    system.dataWriter.dataFile.set(save_fname+".dat")
    system.dataWriter._setOpen(system.dataWriter,system.dataWriter.open,True,1)
    file_l.write(save_fname+"\n")
    file_l.write("Changing "+parameter+": "+str(len(interested_range))+"\n")
    file_l.write("Taking "+str(nFrames)+ " frames per value(planed)\n")
    process=0
    for i in interested_range:
        process+=1
        perc=process*100.0/len(interested_range)
        sys.stdout.write("%d"%perc)
        sys.stdout.write("%\r")
        sys.stdout.flush()
        file_l.write(str(i)+" ")
        eval(set_parameter(parameter,i))
        time.sleep(1.0)
        system.feb.sysReg.timingMode.set(0x0)
        while True:
            if (system.dataWriter._getFrameCount(system.dataWriter,system.dataWriter._getFrameCount)>=process*nFrames):
              #  print("frame number: ",system.dataWriter._getFrameCount(system.dataWriter,system.dataWriter._getFrameCount))
                system.feb.sysReg.timingMode.set(0x3)
                break
    system.dataWriter._setOpen(system.dataWriter,system.dataWriter.open,False,1)
    sys.stdout.write("100%!\n")
    file_l.write("\n end of testing!")
    

def set_parameter(name,value):
    command_set_parameter={'BL':'system.feb.dac.dacBLRaw.set('+str(value)+')','TH':'system.feb.dac.dacPIXTHRaw.set('+str(value)+')'}
    return command_set_parameter[name]

def save_configureFile(file_l,file_s):
    file_l.write(file_s+"\n")
    f_s=open(file_s)
    for line in f_s.readlines(): 
        a=line.split()
        if 'Pixel' not in a[0]:
            if len(a)==2:
                file_l.write("\t"+a[0]+"\t"+a[1]+"\n")
            if len(a)==1:
                file_l.write(a[0]+"\n")

        
