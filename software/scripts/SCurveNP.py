import numpy as np
import ctypes
import matplotlib #.pyplot as plt
import sys
import time
import re
import logging
import copy
import json
import random
from matplotlib import pyplot as plt
import pylab as pl
#import matplotlib.animation as animation
from matplotlib.colors import LogNorm
from matplotlib import cm
from matplotlib import ticker
import scipy.io as sio


#decoding the atlas header of each frame
# jsut return the value needed
def decode_header(frame_rawHeader):
    timestamp=np.uint64()
    frame_size=np.uint32()
    if len(frame_rawHeader)==20:
        for i in range(len(frame_rawHeader)):
            if i==0: 
                Virtual_Channel=frame_rawHeader[i]& 0x1
                Destination_ID_Lane_Z=(frame_rawHeader[i]& 0x7e)>>1
                Transaction_ID_1part=(frame_rawHeader[i]&0xff80)>>7
            if i==1:
                Transaction_ID_2part=frame_rawHeader[i] &0xffff
            if i==2:
                Acquire_Counter=frame_rawHeader[i]&0xffff
            if i==3:
                OP_Code=frame_rawHeader[i] & 0xff
                Element_ID=frame_rawHeader[i] & 0xf00
                Destination_ID_Z=frame_rawHeader[i] & 0xf000
            if i==4:
                Frame_Number_1part=frame_rawHeader[i] & 0xffff
            if i==5:
                Frame_Number_2part=frame_rawHeader[i] & 0xffff
            if i==6:
                Ticks_1part=frame_rawHeader[i] & 0xffff
                timestamp+=Ticks_1part
            if i==7:
                Ticks_2part=frame_rawHeader[i]&0xffff
                timestamp+=Ticks_2part<<16
            if i==8:
                Fiducials_1part=frame_rawHeader[i]&0xffff
                timestamp+=Fiducials_1part<<32
            if i==9:
                Fiducials_2part=frame_rawHeader[i]&0xffff
                timestamp+=Fiducials_2part<<48
            if i==10:
                sbtemp_0=frame_rawHeader[i]&0xffff
            if i==11:
                sbtemp_1=frame_rawHeader[i]&0xffff
            if i==12:
                sbtemp_2=frame_rawHeader[i]&0xffff
            if i==13:
                sbtemp_3=frame_rawHeader[i]&0xffff
            if i==14:
                Frame_Type_1part=frame_rawHeader[i]&0xffff
            if i==15:
                Frame_Type_2part=frame_rawHeader[i]&0xffff

            if i==16:
                frame_size+=(frame_rawHeader[i])<<16
            if i==17:
                frame_size+=frame_rawHeader[i]

        frameSize=int((frame_size)/2)-2
    return timestamp,frameSize

# decode the frame payload in the uint of 16 bit
def decode(TypeOfData,data_temp,frameIndex):
    dvflag_M,mhflag_M,col_M,row_M= 0,0,0,0
    if TypeOfData=="buffer":
        M_det=frameIndex%4
        if int((data_temp & 0x2000)==0):
            dvflag_M, mhflag_M, col_M, row_M = 0,0,0,0
        else:
            dvflag_M, mhflag_M, col_M, row_M = int((data_temp & 0x2000)>0), int((data_temp & 0x1000)>0), (data_temp & 0x0f80)>>7, data_temp & 0x007F # data_temp[13],data_temp[12],[11:7],[6:0]
    return M_det,dvflag_M,mhflag_M,col_M,row_M


class frame_data:
    def __init__(self):
        self.dvflag_M0=[]
        self.mhflag_M0=[]
        self.col_M0=[]
        self.row_M0=[]
    
        self.dvflag_M1=[]
        self.mhflag_M1=[]
        self.col_M1=[]
        self.row_M1=[]

        self.dvflag_M2=[]
        self.mhflag_M2=[]
        self.col_M2=[]
        self.row_M2=[]
       
        self.hitmap_t0=np.zeros((128,32))
        self.hitmap_t1=np.zeros((128,32))
        self.hitmap_t2=np.zeros((128,32))
        
        self.comm = {'0':self.add_on_M0, '1':self.add_on_M1, '2':self.add_on_M2}

    def add_data(self,TypeOfData,data_temp,frameIndex):
        M_t, dvflag_M_t, mhflag_M_t, col_M_t, row_M_t=decode(TypeOfData,data_temp,frameIndex)   
        if dvflag_M_t!=0:
            self.comm.get(str(M_t))(dvflag_M_t, mhflag_M_t, col_M_t, row_M_t)
   
    def add_data_with_return(self,TypeOfData,data_temp,frameIndex):
        M_t, dvflag_M_t, mhflag_M_t, col_M_t, row_M_t=decode(TypeOfData,data_temp,frameIndex)   
        if dvflag_M_t!=0:
            self.comm.get(str(M_t))(dvflag_M_t, mhflag_M_t, col_M_t, row_M_t)
            return M_t,dvflag_M_t,mhflag_M_t,col_M_t,row_M_t
        else:
            return 0,0,0,0,0

    def add_on_M0(self,dvflag_M_i, mhflag_M_i, col_M_i, row_M_i): 
        self.dvflag_M0.append(dvflag_M_i)
        self.mhflag_M0.append(mhflag_M_i)
        self.col_M0.append(col_M_i)
        self.row_M0.append(row_M_i)
        self.hitmap_t0[row_M_i][col_M_i]+=1
        
    def add_on_M1(self,dvflag_M_i, mhflag_M_i, col_M_i, row_M_i):
        self.dvflag_M1.append(dvflag_M_i)
        self.mhflag_M1.append(mhflag_M_i)
        self.col_M1.append(col_M_i)
        self.row_M1.append(row_M_i)
        self.hitmap_t1[row_M_i][col_M_i]+=1

    def add_on_M2(self,dvflag_M_i, mhflag_M_i, col_M_i, row_M_i):
        self.dvflag_M2.append(dvflag_M_i)
        self.mhflag_M2.append(mhflag_M_i)
        self.col_M2.append(col_M_i)
        self.row_M2.append(row_M_i)
        self.hitmap_t2[row_M_i][col_M_i]+=1


def get_frame_header(file_o):
    file_header=np.fromfile(file_o,dtype='uint32',count=2)
    return file_header

# help to check the stream readout speed
# check the consecution of the frames
# return the efficiency: missed frames/ total frames received
def check_SR_file(file_o):
    frame_num=-1
    file_finished=1
    time_stamp_all=[]
    missed_frames=0
    frame_acquire_number=[0,0]
    missed_time=[]
    while(file_finished):
        file_header=get_frame_header(file_o)
        frame_num+=1
        if len(file_header)==0:
            file_finished=0
            break
        frame_Size = int(file_header[0]/2)-2
        frame_rawData,frame_rawHeader,frame_all,time_stamp=get_frame(file_o,frame_Size)
        if frame_num==0: t_0=(frame_rawHeader[2] &0xffff)
        frame_acquire_number.append(frame_rawHeader[2] &0xffff)
        frame_acquire_number.remove(frame_acquire_number[0]) 
        missed_time.append((frame_rawHeader[2] &0xffff)-t_0)
        if (frame_acquire_number[0]!=0 and frame_acquire_number[1]!=0):
            if (frame_acquire_number[1]-frame_acquire_number[0])>1:
                missed_frames+=1
        time_stamp_all.append(time_stamp)

    return missed_time,missed_frames,frame_num,time_stamp_all 


def get_frame(file_o,frame_size,debug=0):
    PayLoad=np.fromfile(file_o,dtype='uint16',count=frame_size)
    frame_rawHeader=PayLoad[0:16].copy()
    frame_rawData=PayLoad[16:].copy()
    frame_all=PayLoad.copy()
    timestamp=np.uint64()
    for i in range(len(frame_rawHeader)):
        #print ("frame header: ",bin(i)[2:].rjust(16,"0"))
        if debug:
            print ("frame header----: ",bin(frame_rawHeader[i])[2:].rjust(16,"0"))
        if i==0: 
            if debug:
                print("Virtual Channel: ",(frame_rawHeader[i]& 0x1))
                print("Destination ID (Lane +Z): ",(frame_rawHeader[i]& 0x7e)>>1)
                print("Transaction ID 1part: ",(frame_rawHeader[i]&0xff80)>>7)
        if i==1:
            if debug:
                print("Transaction ID 2part: ",frame_rawHeader[i] &0xffff)
        if i==2:
            if debug:
                print("Acquire Counter: ",frame_rawHeader[i]&0xffff)
        if i==3:
            if debug:
                print("OP Code: ",frame_rawHeader[i] & 0xff)
                print("Element ID: ",frame_rawHeader[i] & 0xf00)
                print("Destination ID (Z only): ",frame_rawHeader[i] & 0xf000)     
        if i==4:
            if debug:
                print("Frame Number 1part: ",frame_rawHeader[i] & 0xffff)
        if i==5:
            if debug:
                print("Frame Number 2part: ",frame_rawHeader[i] & 0xffff)
        if i==6:
            if debug:
                print("Ticks 1part: ",frame_rawHeader[i] & 0xffff)
            timing_1=frame_rawHeader[i] & 0xffff
            timestamp+=timing_1
        if i==7:
            if debug:
                print("Ticks 2part: ",frame_rawHeader[i]&0xffff)
            timing_2=frame_rawHeader[i] & 0xffff
            timestamp+=timing_2<<16
        if i==8:
            if debug:
                print("Fiducials 1part: ",frame_rawHeader[i]&0xffff)
            timing_3=frame_rawHeader[i] & 0xffff
            timestamp+=timing_3<<32
        if i==9:
            if debug:
                print("Fiducials 2part: ",frame_rawHeader[i]&0xffff)
            timing_4=frame_rawHeader[i] & 0xffff
            timestamp+=timing_4<<48
        if i==10:
            if debug:
                print("sbtemp[0]: ",frame_rawHeader[i]&0xffff)
        if i==11:
            if debug:
                print("sbtemp[1]: ",frame_rawHeader[i]&0xffff)
        if i==12:
            if debug:
                print("sbtemp[2]: ",frame_rawHeader[i]&0xffff)
        if i==13:
            if debug:
                print("sbtemp[3]: ",frame_rawHeader[i]&0xffff)
        if i==14:
            if debug:
                print("Frame Type 1part: ",frame_rawHeader[i]&0xffff)
        if i==15:
            if debug:
                print("Frame Type 2part: ",frame_rawHeader[i]&0xffff)
    if debug:
        print("timestamp: ",timestamp)
    return frame_rawData,frame_rawHeader,frame_all,timestamp

#data class for register reading
class timep:
    def __init__(self,pixel1,matrix1,index1,threshold1,time1):
        self.pixel=pixel1
        self.matrix=matrix1
        self.index=index1
        self.threshold=threshold1
        self.time=time1

def logfile(logfilename):
    logger=logging.getLogger()
    LOG_FILE=logfilename
    LOG_FORMAT="%(asctime)s : %(funcName)s: %(message)s"
    logging.basicConfig(filename=LOG_FILE,level=logging.DEBUG, format=LOG_FORMAT)
    return logger

def binRep(num):
    #binNum = bin(ctypes.c_uint.from_buffer(ctypes.c_float(num)).value)
    binNum = bin(ctypes.c_uint.from_buffer(ctypes.c_float(num)).value)[2:]
    print("bits: " + binNum.rjust(32,"0"))
    return binNum.rjust(32,"0")

#load register reading results file (.json)
def load_chess2_data(filename):
    for i in [2]:
        file_data=open(filename,'r')
        for line in file_data.readlines():
            if ('Shape' in line):
                shape_hist=re.findall('\d+',line)
               # print(len(shape_hist))
                break
        data_1d=np.loadtxt(sys.argv[1])
        hists=data_1d.reshape(int(shape_hist[0]),int(shape_hist[1]),int(shape_hist[2]),int(shape_hist[3]))	
    return hists

def get_pixelsandthresholds(filename):
    file_data=open(filename,'r')
    pixels=[]
    for line in file_data.readlines():
        a=re.findall('"pixel":..........',line)
        threshold=re.findall('"threshold":.........',line)
        thresholds=[]
        for j in range(len(threshold)):
            threshold_i=re.findall(r"\d+\:?\d*",threshold[j])
            threshold_t=int(threshold_i[0])
            if (threshold_t in thresholds):
                continue
            thresholds.append(threshold_t)
        thresholds.sort()
        b=len(a)
        a1_i=0
        a1=[]
        for b_i in range(b):
            if b_i==0:
                a1.append(a[b_i])
            else:
                if a[b_i]!=a1[-1]:
                    a1.append(a[b_i])
        for i in range(len(a1)):
            pixel_i=re.findall(r"\d+\:?\d*",a1[i])
            p_2=(int(pixel_i[0]),int(pixel_i[1]))
            pixels.append(p_2)
    return pixels,thresholds

def get_values(filename):
    file_data=open(sys.argv[1],'r')
    line_count=0
    start=False
    for line in file_data.readlines():
        line_count+=1
        if ('thresholds (raw)' in line):
            thresholds=re.findall('\d+',line)
            start_line=line_count
            start=True
        if (start):
            if (line_count>start_line):
                if (not (']' in line)):
                    thresholds1=re.findall('\d+',line)
                    thresholds.extend(thresholds1)
                else: 
                    thresholds1=re.findall('\d+',line)
                    thresholds.extend(thresholds1)
                    break
    file_data=open(sys.argv[1],'r')
    for line in file_data.readlines():
        if ('PulseDelay:' in line):
            PulseDelay=re.findall('\d+',line)
            break
    file_data=open(sys.argv[1],'r')
    for line in file_data.readlines():
        if ('PulseWidth:' in line):
            PulseWidth=re.findall('\d+',line)
            break
    return thresholds,PulseDelay[0],PulseWidth[0]
       
""" The following test enables to test a set of pixels with different interested parameters, in this case the paramter is Threshold"""

def makeCalibCurve4(system,nCounts,thresholdCuts,pixels=None,histFileName="scurve.root", deltaBLToBLR = 608, chargeInjectionEnbled = 0, BL=0x26c,Reading_all_pixel_together= False,mode=0):
    logging.info("Using makeCalibCurve4......")
    pixEnable = 1
    chargeInj1 = not chargeInjectionEnbled  # 0 - enable / 1 - disabled
    trim = 7
    system.feb.chargeInj.calPulseInh.set(chargeInj1)
    print("Disable all pixels")
    system.feb.Chess2Ctrl0.writeAllPixels(enable= 0,chargeInj= 1,trimI= trim)
    system.feb.Chess2Ctrl1.writeAllPixels(enable= 0,chargeInj= 1,trimI= trim)
    system.feb.Chess2Ctrl2.writeAllPixels(enable= 0,chargeInj= 1,trimI= trim)
    print("Trim, pixEnable, chargeInj: (%i,%i,%i)"%(trim, pixEnable, chargeInj1))
    if Reading_all_pixel_together:
        print("reading all together")
        hists = makeCalibCurveLoopBLx_8hits(system,nCounts,thresholdCuts,pixels,histFileName, pixEnableLogic = pixEnable, chargeInjLogic = chargeInj1, pixTrimI = trim, deltaBLToBLR = deltaBLToBLR,BL_v=BL,mode=mode)
    else:
        print("generating hitmap")
        hists = makeCalibCurveLoopBLx_8hits_hitmap(system,nCounts,thresholdCuts,pixels,histFileName, pixEnableLogic = pixEnable, chargeInjLogic = chargeInj1, pixTrimI = trim, deltaBLToBLR = deltaBLToBLR,BL_v=BL)
        
    return hists

#return an empty dictionary for the data
def get_allHists(pixels,matrix,indexs,thresholdCuts):
    allHist={}.fromkeys(pixels)
    for pixel in pixels:
        allHist[pixel]={}.fromkeys(matrix)
        for matri in matrix:
            allHist[pixel][matri]={}.fromkeys(indexs)
            for index in indexs:
                allHist[pixel][matri][index]={}.fromkeys(thresholdCuts)
                for threshold in thresholdCuts:
                    allHist[pixel][matri][index][threshold]=[]
    return allHist

def dic2timep(dic):
    return timep(dic['pixel'],dic['matrix'],dic['index'],dic['threshold'],dic['time'])

def timep2dic(timep):
    return {'pixel':timep.pixel,'matrix':timep.matrix,'index':timep.index,'threshold':timep.threshold,'time':timep.time}

def save_f_json(file_name,hists):
    with open(file_name+'.json','w',encoding='utf-8') as f:
        json.dump(hists,f,default=timep2dic)

def save_timep(hists):
    allhist=[]
    for key in hists: #pixel
        print(key)
        for key1 in hists[key]: #matrix
            for key2 in hists[key][key1]: #index
                for key3 in hists[key][key1][key2]: #threshold
                    one=timep(key,key1,key2,key3,hists[key][key1][key2][key3])
                    allhist.append(one)
    return allhist

def makeCalibCurveLoopBLx_8hits(system,nCounts,thresholdCuts,pixels=None,histFileName="scurve.root",pixEnableLogic=1,chargeInjLogic=0,pixTrimI=0,deltaBLToBLR=608,BL_v=0x800,mode=0):
    nColumns      = 32
    nRows         = 128
    logging.info(" Using makeCalibCurveLoopBLx_8hits......")
    real_data=mode #1: real size display, 2 hitmap display
    matrix=[0,1,2]
    hits=[0,1,2,3,4,5,6,7]
    pixels = pixels if (pixels!=None) else [ (row,col) for row in range(1,128,1) for col in range(1,32,1) ]
    eventdump=False
    if len(thresholdCuts)==1:
        eventdump=True
    allHists=get_allHists(pixels,matrix,hits,thresholdCuts)
    BLRValue  = BL_v + deltaBLToBLR
    #BLRValue=0x672
    system.feb.dac.dacBLRRaw.set(BLRValue)
    print("Thresholds (system.feb.dac.dacBLRRaw): ",  hex(BLRValue))
    system.feb.dac.dacBLRaw.set(BL_v)
    print("Thresholds (system.feb.dac.dacBLRaw): ",  hex(BL_v))
    time_h=200000
    time_reso=1000
    time_bin=range(0,time_h,time_reso)
    d_time=0
    d_time_2=time_h
    time.sleep(2.0)
    if real_data==2:
        plt.ion()
        fig_all=plt.subplots(figsize=(11,9))
    if real_data==1:
        plt.ion()
        figure_0,ax=plt.subplots(figsize=(11,9))
        ax.set_axis_off()
        chass2_point=[(87.9,108),(20228,108),(24300,108),(24300,18517),(24300,18517),(20227,18517),(87.9,18517),(87.9,13413),(87.9,13138),(87.9,8034),(87.9,5212),(20227,5212),(20227,8034),(20227,13138),(20227,13413)]
        for i in range(9):
            ax.plot([chass2_point[i][0],chass2_point[i+1][0]],[chass2_point[i][1],chass2_point[i+1][1]],'k')
        ax.plot([chass2_point[0][0],chass2_point[9][0]],[chass2_point[0][1],chass2_point[9][1]],'k')
        ax.plot([chass2_point[1][0],chass2_point[5][0]],[chass2_point[1][1],chass2_point[5][1]],'k')
        for i in range(7,12,1):
            ax.plot([chass2_point[i][0],chass2_point[21-i][0]],[chass2_point[i][1],chass2_point[21-i][1]],'k')
        plt.show()
        plt.ion()
        figure_1,ax1=plt.subplots(figsize=(13,8))
        ax1.set_axis_off()
        #fig_all=plt.figure(figsize=(17,10))
    hitmap_t0=np.zeros((nRows,nColumns))
    hitmap_t1=np.zeros((nRows,nColumns))
    hitmap_t2=np.zeros((nRows,nColumns))
    time_inde=range(0,time_h,time_reso) 
    time_t=np.zeros((4,len(time_inde)))
    time_t[0]=time_inde
 
    thre_t=np.zeros((4,len(thresholdCuts)))
    thre_t[0]=np.asarray(thresholdCuts)/1241.
    time_buffer=time_t
    thre_buffer=thre_t
    thre_index=0
    hot_pixels_m0=[(0,0)]
    hot_pixels_m1=[(0,0)]
    hot_pixels_m2=[(0,0)]
  
    for (row,col) in pixels:
        if (row,col) in hot_pixels_m0:
            print("hot pixel on Matrix 0: (%i,%i)"%(row,col))
        else:
            system.feb.Chess2Ctrl0.writePixel(enable=pixEnableLogic, chargeInj=chargeInjLogic, col=col, row=row, trimI= pixTrimI)
        if (row,col) in hot_pixels_m1:
            print("hot pixel on Matrix 1: (%i,%i)"%(row,col))
        else:
            system.feb.Chess2Ctrl1.writePixel(enable=pixEnableLogic, chargeInj=chargeInjLogic, col=col, row=row, trimI= pixTrimI)
        if (row,col) in hot_pixels_m2:
            print("hot pixel on Matrix 2: (%i,%i)"%(row,col))
        else:
            system.feb.Chess2Ctrl2.writePixel(enable=pixEnableLogic, chargeInj=chargeInjLogic, col=col, row=row, trimI= pixTrimI)
    for threshold in thresholdCuts:
        print("Thresholds (system.feb.dac.dacPIXTHRaw): ",  hex(threshold))
        system.feb.dac.dacPIXTHRaw.set(threshold)
        time.sleep(2.0)
        print("start taking ",nCounts," counts :", time.clock())
        for cnt in range(nCounts):
            system.feb.chargeInj.calPulse.set(1)
            system.ReadAll()
            for n in [1]:
                for hit in hits:
                    matrix_i=0
                    if eval(get_funct('Valid',matrix_i,hit)):
                        row_det = int(eval(get_funct('row_det',matrix_i,hit)))
                        col_det = int(eval(get_funct('col_det',matrix_i,hit)))
                        time_m0=  float(eval(get_funct('time_det',matrix_i,hit)))
                        if (time_m0<time_h):
                            if (row_det,col_det) in pixels:
                                print("row_det: ",row_det, "col_det:", col_det, "system.feb.chargeInj.hitDetTime"+str(matrix_i)+"_"+str(hit)+":", time_m0)
                                allHists[(row_det,col_det)][matrix_i][hit][threshold].append(float(eval(get_funct('time_det',matrix_i,hit))))
                            #else:
                               # allHists[(row_det,col_det)][matrix_i][hit][threshold].append(float(-2.0))
                                if (d_time<time_m0<d_time_2):                       
                                    time_buffer[matrix_i+1][int(time_m0/time_reso)]+=1
                                    thre_buffer[matrix_i+1][thre_index]+=1
                                    hitmap_t0[row_det][col_det]+=1
                    matrix_i=1
                    if eval(get_funct('Valid',matrix_i,hit)):
                        row_det = int(eval(get_funct('row_det',matrix_i,hit)))
                        col_det = int(eval(get_funct('col_det',matrix_i,hit)))
                        time_m1=float(eval(get_funct('time_det',matrix_i,hit)))
                        if (time_m1<time_h):
                           # print("row_det: ",row_det, "col_det:", col_det, "system.feb.chargeInj.hitDetTime"+str(matrix_i)+"_"+str(hit)+":", time_m1)
                            if (row_det,col_det) in pixels:
                                print("row_det: ",row_det, "col_det:", col_det, "system.feb.chargeInj.hitDetTime"+str(matrix_i)+"_"+str(hit)+":", time_m1)
                                allHists[(row_det,col_det)][matrix_i][hit][threshold].append(float(eval(get_funct('time_det',matrix_i,hit))))
                            #else:
                                #allHists[(row_det,col_det)][matrix_i][hit][threshold].append(float(-2.0))
                                if (d_time<time_m1<d_time_2):                       
                                    time_buffer[matrix_i+1][int(time_m1/time_reso)]+=1
                                    thre_buffer[matrix_i+1][thre_index]+=1
                                    hitmap_t1[row_det][col_det]+=1
                    matrix_i=2
                    if eval(get_funct('Valid',matrix_i,hit)):
                        row_det = int(eval(get_funct('row_det',matrix_i,hit)))
                        col_det = int(eval(get_funct('col_det',matrix_i,hit)))
                        time_m2=float(eval(get_funct('time_det',matrix_i,hit)))
            #            OutputFile.write("("+str(row_det_raw)+","+str(col_det_raw)+"):  ")
            #            OutputFile.write(str(time_m2_raw)+"\n")
                        if (time_m2<time_h):
                            #print("row_det: ",row_det, "col_det:", col_det, "system.feb.chargeInj.hitDetTime"+str(matrix_i)+"_"+str(hit)+":", time_m2)
                        #if (row_det,col_det) in (row,col):
                            if (row_det,col_det) in pixels:
                                print("row_det: ",row_det, "col_det:", col_det, "system.feb.chargeInj.hitDetTime"+str(matrix_i)+"_"+str(hit)+":", time_m2)
                                allHists[(row_det,col_det)][matrix_i][hit][threshold].append(float(eval(get_funct('time_det',matrix_i,hit))))
                            #else:
                                #allHists[(row_det,col_det)][matrix_i][hit][threshold].append(float(-2.0))
                                if (d_time<time_m2<d_time_2):                       
                                    time_buffer[matrix_i+1][int(time_m2/time_reso)]+=1
                                    thre_buffer[matrix_i+1][thre_index]+=1
                                    hitmap_t2[row_det][col_det]+=1
        print("finishing taking ",nCounts," counts :", time.clock())
        print("updating plots :", time.clock())
        thre_index+=1
        if real_data==1:  #real_size event display
            l_size=10
            pl.figure(1)
            ax0=figure_0.add_axes([0.16,0.144,0.586,0.1955])
            ax0.clear()
            plt.imshow(hitmap_t2,aspect="auto",cmap='gray',origin='upper',vmin=0,interpolation='nearest')
            ax1=figure_0.add_axes([0.16,0.444,0.586,0.1955])
            ax1.clear()
            plt.imshow(hitmap_t1,aspect="auto",cmap='gray',origin='upper',vmin=0,interpolation='nearest')
            ax2=figure_0.add_axes([0.16,0.6485,0.586,0.1955])
            ax2.clear()
            plt.imshow(hitmap_t0,aspect="auto",cmap='gray',origin='lower',vmin=0,interpolation='nearest')
            #plt.show()
            figure_0.canvas.draw()
            figure_0.canvas.flush_events()
            pl.figure(2)
            fig_2_time=plt.subplot(2,1,1)
            fig_2_time.cla() 
            plt.plot(time_buffer[0],time_buffer[1],'b--',label='Matrix 0: time distribution')
            plt.plot(time_buffer[0],time_buffer[2],'y-.',label='Matrix 1: time distribution')
            plt.plot(time_buffer[0],time_buffer[3],'r-',label='Matrix 2: time distribution')
            plt.legend()
            plt.xlabel('Time [ns]',fontsize=l_size)
            plt.ylabel('Counts',fontsize=l_size)
            plt.gca().xaxis.get_major_formatter().set_powerlimits((0,200))
            fig_2_thre=plt.subplot(2,1,2)
            fig_2_thre.cla() 
            plt.step(thre_buffer[0],thre_buffer[1],'b--',label='Matrix 0: threshold scan')
            plt.step(thre_buffer[0],thre_buffer[2],'y-.',label='Matrix 1: threshold scan')
            plt.step(thre_buffer[0],thre_buffer[3],'r-',label='Matrix 2: threshold scan')
            plt.legend()
            plt.xlabel('Threshold [V]',fontsize=l_size)
            plt.ylabel('Counts',fontsize=l_size)
            figure_1.canvas.draw()
            figure_1.canvas.flush_events()
            print("finish updating plots :", time.clock())
    allhist=save_timep(allHists)
    return allhist

def makeCalibCurveLoopBLx_8hits_hitmap(system,nCounts,thresholdCuts,pixels=None,histFileName="scurve.root",pixEnableLogic=1,chargeInjLogic=0,pixTrimI=0,deltaBLToBLR=608,BL_v=0x800):
    nColumns      = 32
    nRows         = 128
    logging.info(" Using makeCalibCurveLoopBLx_8hits_hitmap......")
    matrix=[0,1,2]
    hits=[0,1,2,3,4,5,6,7]
    pixels = pixels if (pixels!=None) else [ (row,col) for row in range(0,nRows,1) for col in range(0,nColumns,1) ]
    allHists=get_allHists(pixels,matrix,hits,thresholdCuts)
    BLRValue  = BL_v + deltaBLToBLR
    system.feb.dac.dacBLRRaw.set(BLRValue)
    print("Thresholds (system.feb.dac.dacBLRRaw): ",  hex(BLRValue))
    system.feb.dac.dacBLRaw.set(BL_v)
    print("Thresholds (system.feb.dac.dacBLRaw): ",  hex(BL_v))
    time_h=200000
    time_reso=1000
    d_time=0
    d_time_2=time_h
    time_bin=range(0,time_h,time_reso)
    hitmap_t0=np.zeros((nRows,nColumns))
    hitmap_t1=np.zeros((nRows,nColumns))
    hitmap_t2=np.zeros((nRows,nColumns))
    hitmap_t0_a=np.zeros((nRows,nColumns))
    hitmap_t1_a=np.zeros((nRows,nColumns))
    hitmap_t2_a=np.zeros((nRows,nColumns))
    time_inde=range(0,time_h,time_reso) 
    time_t=np.zeros((4,len(time_inde)))
    time_t[0]=time_inde
    #plt.ion()
    #fig_all=plt.figure(figsize=(17,10))
 
    thre_t=np.zeros((4,len(thresholdCuts)))
    thre_t[0]=np.asarray(thresholdCuts)/1241.
    time_buffer=time_t
    thre_buffer=thre_t
    hot_pixels=[(27,16),(50,15),(45,15)]
    #chargeInjLogic=1
    for (row,col) in pixels:
        if (row,col) in hot_pixels:
            print("hot pixel: (%i,%i)"%(row,col))
        else:
            print("enable Pixel: (%i,%i)"%(row,col))
            system.feb.Chess2Ctrl0.writePixel(enable=pixEnableLogic, chargeInj=chargeInjLogic, col=col, row=row, trimI= pixTrimI)
            system.feb.Chess2Ctrl1.writePixel(enable=pixEnableLogic, chargeInj=chargeInjLogic, col=col, row=row, trimI= pixTrimI)
            system.feb.Chess2Ctrl2.writePixel(enable=pixEnableLogic, chargeInj=chargeInjLogic, col=col, row=row, trimI= pixTrimI)
            thre_index=0
            
            for threshold in thresholdCuts:
                print("Thresholds (system.feb.dac.dacPIXTHRaw): ",  hex(threshold))
                print("time start setting threshold: ", time.clock())
                system.feb.dac.dacPIXTHRaw.set(threshold)
                print("time start finishing threshold: ", time.clock())
                time.sleep(2.0)
                print("time after sleep(2.0): ", time.clock())
                system.ReadAll()
                print("time after readall(): ", time.clock())
                print("start taking ",nCounts," counts :", time.clock())
                for cnt in range(nCounts):
                    system.feb.chargeInj.calPulseVar.set(1)
                    #time.sleep(0.05)
                    system.ReadAll()
                    for n in [1]:
                        for hit in hits:
                            matrix_i=0
                            if eval(get_funct('Valid',matrix_i,hit)):
                                row_det = int(eval(get_funct('row_det',matrix_i,hit)))
                                col_det = int(eval(get_funct('col_det',matrix_i,hit)))
                                time_m0=float(eval(get_funct('time_det',matrix_i,hit)))
                                if (row_det==row and col_det==col):
                                    allHists[(row_det,col_det)][matrix_i][hit][threshold].append(float(eval(get_funct('time_det',matrix_i,hit))))
                                    #allHists[(row_det,col_det)][matrix_i][hit][threshold].append(time_m0)
                                    if (time_m0<time_h):
                                        print("row_det: ",row_det, "col_det:", col_det, "system.feb.chargeInj.hitDetTime"+str(matrix_i)+"_"+str(hit)+":", time_m0)
                                        if (d_time<time_m0<d_time_2):                       
                                            time_buffer[matrix_i+1][int(time_m0/time_reso)]+=1
                                            thre_buffer[matrix_i+1][thre_index]+=1
                                            hitmap_t0[row_det][col_det]+=1
                                else:
                                    allHists[(row,col)][matrix_i][hit][threshold].append(float(-2.0))
                            else: 
                                allHists[(row,col)][matrix_i][hit][threshold].append(float(-1.0))
                            matrix_i=1
                            if eval(get_funct('Valid',matrix_i,hit)):
                                row_det = int(eval(get_funct('row_det',matrix_i,hit)))
                                col_det = int(eval(get_funct('col_det',matrix_i,hit)))
                                time_m1=float(eval(get_funct('time_det',matrix_i,hit)))
                                if (row_det==row and col_det==col):
                                    allHists[(row_det,col_det)][matrix_i][hit][threshold].append(time_m1)
                                    if (time_m1<time_h):
                                        print("row_det: ",row_det, "col_det: ", col_det, "system.feb.chargeInj.hitDetTime"+str(matrix_i)+"_"+str(hit)+":", time_m1)
                                        if (d_time<time_m1<d_time_2):                       
                                            time_buffer[matrix_i+1][int(time_m1/time_reso)]+=1
                                            thre_buffer[matrix_i+1][thre_index]+=1
                                            hitmap_t1[row_det][col_det]+=1
                                else:
                                    allHists[(row,col)][matrix_i][hit][threshold].append(float(-2.0))
                            else: 
                                allHists[(row,col)][matrix_i][hit][threshold].append(float(-1.0))
                            matrix_i=2
                            if eval(get_funct('Valid',matrix_i,hit)):
                                row_det = int(eval(get_funct('row_det',matrix_i,hit)))
                                col_det = int(eval(get_funct('col_det',matrix_i,hit)))
                                time_m2=float(eval(get_funct('time_det',matrix_i,hit)))
                                if (row_det==row and col_det==col):
                                    allHists[(row_det,col_det)][matrix_i][hit][threshold].append(time_m2)
                                    if (time_m2<time_h):
                                        print("row_det: ",row_det, "col_det: ", col_det, "system.feb.chargeInj.hitDetTime"+str(matrix_i)+"_"+str(hit)+":", time_m2)
                                        if (d_time<time_m2<d_time_2):                       
                                            time_buffer[matrix_i+1][int(time_m2/time_reso)]+=1
                                            thre_buffer[matrix_i+1][thre_index]+=1
                                            hitmap_t2[row_det][col_det]+=1
                                else:
                                    allHists[(row,col)][matrix_i][hit][threshold].append(float(-2.0))
                            else: 
                                allHists[(row,col)][matrix_i][hit][threshold].append(float(-1.0))
                thre_index+=1
                l_size=10
        system.feb.Chess2Ctrl0.writePixel(enable=not pixEnableLogic, chargeInj=chargeInjLogic, col=col, row=row)
        system.feb.Chess2Ctrl1.writePixel(enable=not pixEnableLogic, chargeInj=chargeInjLogic, col=col, row=row)
        system.feb.Chess2Ctrl2.writePixel(enable=not pixEnableLogic, chargeInj=chargeInjLogic, col=col, row=row)
        print("disable Pixel: (%i,%i)"%(row,col))
    find_hotpixel=False
    if find_hotpixel:
        plt.ion()
        fig_all=plt.figure(figsize=(17,8))
        fig_0_hmp=plt.subplot(3,2,1)
        plt.imshow(hitmap_t0,aspect="auto",cmap='rainbow',origin=[0,0],extent=[0,31,0,127],interpolation='nearest')
        plt.xlabel('Row',fontsize=l_size)
        plt.ylabel('Column',fontsize=l_size)
        plt.colorbar()
        fig_0_hmp_a=plt.subplot(3,2,2)
        plt.imshow(hitmap_t0_a,aspect="auto",cmap='rainbow',origin=[0,0],extent=[0,31,0,127],interpolation='nearest')
        plt.xlabel('Row',fontsize=l_size)
        plt.ylabel('Column',fontsize=l_size)
        plt.colorbar()
        fig_1_hmp=plt.subplot(3,2,3)
        plt.imshow(hitmap_t1,aspect="auto",cmap='rainbow',origin=[0,0],extent=[0,31,0,127],interpolation='nearest')
        plt.xlabel('Row',fontsize=l_size)
        plt.ylabel('Column',fontsize=l_size)
        plt.colorbar()
        fig_1_hmp_a=plt.subplot(3,2,4)
        plt.imshow(hitmap_t1_a,aspect="auto",cmap='rainbow',origin=[0,0],extent=[0,31,0,127],interpolation='nearest')
        plt.xlabel('Row',fontsize=l_size)
        plt.ylabel('Column',fontsize=l_size)
        plt.colorbar()
        fig_2_hmp=plt.subplot(3,2,5)
        plt.imshow(hitmap_t2,aspect="auto",cmap='rainbow',origin=[0,0],extent=[0,31,0,127],interpolation='nearest')
        plt.xlabel('Row',fontsize=l_size)
        plt.ylabel('Column',fontsize=l_size)
        plt.colorbar()
        fig_2_hmp_a=plt.subplot(3,2,6)
        plt.imshow(hitmap_t2_a,aspect="auto",cmap='rainbow',origin=[0,0],extent=[0,31,0,127],interpolation='nearest')
        plt.xlabel('Row',fontsize=l_size)
        plt.ylabel('Column',fontsize=l_size)
        plt.colorbar()
        fig_all.canvas.draw()
    allhist=save_timep(allHists)
    return allhist

def get_funct(name,matrix,hit):
    name_d={'Valid':'system.feb.chargeInj.hitDetValid'+str(matrix)+'_'+str(hit)+'.get()','row_det':'system.feb.chargeInj.hitDetRow'+str(matrix)+'_'+str(hit)+'.get()','col_det':'system.feb.chargeInj.hitDetCol'+str(matrix)+'_'+str(hit)+'.get()','time_det':'system.feb.chargeInj.hitDetTime'+str(matrix)+'_'+str(hit)+'.get()','time_det_raw':'system.feb.chargeInj.hitDetTimeRaw'+str(matrix)+'_'+str(hit)+'.get()'}
    return name_d[name]

def data_update_Ri(Ri,t1):
    if (time.clock-t1)%100==0:
        if(Ri):
            print('updating Ri')
            return Ri


