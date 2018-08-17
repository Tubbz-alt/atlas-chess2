import sys
sys.path.append("../../")
from SCurveNP import *
from ROOT import *
from ROOT import gROOT, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TLorentzVector, TGraphErrors, TGraph
from ROOT import TPad, TPaveText, TLegend, THStack
from ROOT import gBenchmark, gStyle, gROOT, gPad
import re
import os
import numpy as np
from array import array
import matplotlib.pyplot as plt

def data_ana(arg):
    
    conf_filename, data_filenames = check_DataFileNumber(sys.argv[1])
    if len(data_filenames)>0:
        Sweep_parameter,Steps,frames_perstep,par,conf_dic=ReadConfigure(conf_filename)
        nCols = 32
        nRows = 128
        root_f = TFile(sys.argv[1]+'.root',"RECREATE") 
        #TH2D *H_P0[Steps]
        #TH2D *H_P1[Steps]
        #TH2D *H_P2[Steps]
        nn=Sweep_parameter
        th1=";Frames;"+Sweep_parameter+"_Values"
        Para_h=TH1D(Sweep_parameter,th1,int(Steps),0,int(par[-1]))
        TH3D_Axis=";Row;Col;"+Sweep_parameter+"_Values"
        Hitmap_M0_3d=TH3D("Matrix0_3D_HitMap",TH3D_Axis,nCols,0,nCols,nRows,0,nRows,int(Steps),0,int(par[-1]))
        Hitmap_M1_3d=TH3D("Matrix1_3D_HitMap",TH3D_Axis,nCols,0,nCols,nRows,0,nRows,int(Steps),0,int(par[-1]))
        Hitmap_M2_3d=TH3D("Matrix2_3D_HitMap",TH3D_Axis,nCols,0,nCols,nRows,0,nRows,int(Steps),0,int(par[-1]))
        #Para_h=TH1D(str(Sweep_parameter),";Frames;Values",Steps,0,int(par[-1]))
        H_P0=[]
        H_P1=[]
        H_P2=[]
        for i_p in range(int(Steps)):
            H_P0.append("Chess2_Matrix0_hitmap_"+Sweep_parameter+"_at_"+par[i_p])
            H_P1.append("Chess2_Matrix1_hitmap_"+Sweep_parameter+"_at_"+par[i_p])
            H_P2.append("Chess2_Matrix2_hitmap_"+Sweep_parameter+"_at_"+par[i_p])
        for i_p in range(int(Steps)):
            H_P_name='Matrix0_Hitmap_with_'+Sweep_parameter+'_at_'+par[i_p]
            H_P_name1='Matrix1_Hitmap_with_'+Sweep_parameter+'_at_'+par[i_p]
            H_P_name2='Matrix2_Hitmap_with_'+Sweep_parameter+'_at_'+par[i_p]
            H_P0[i_p]=TH2D(H_P_name,";Row;Col",nCols,0,nCols,nRows,0,nRows)
            H_P1[i_p]=TH2D(H_P_name1,";Row;Col",nCols,0,nCols,nRows,0,nRows)
            H_P2[i_p]=TH2D(H_P_name2,";Row;Col",nCols,0,nCols,nRows,0,nRows)
       
        #data_tree = TTree("data_tree"," data for chess2")
        
        #para=np.zeros(1,dtype=float)
        hitmap_m0=np.zeros(shape=(128,32))
        hitmap_m1=np.zeros(shape=(128,32))
        hitmap_m2=np.zeros(shape=(128,32))
        #time_all=np.array("f",[])

        #data_tree.Branch('normal',time_all,'normal/F')
        #data_tree.Branch('hitmap_M0',hitmap_m0,'hitmap_M0/I')
        #data_tree.Branch('hitmap_M1',hitmap_m1,'hitmap_M1/I')
        #data_tree.Branch('hitmap_M2',hitmap_m2,'hitmap_M2/I')
        #data_tree.Branch('paramter_interested',para,'p')
        alldata=frame_data()
        allFrame=[]
        frame_header=[0]    
        time_all=[]
        for data_filePro in data_filenames:
            print "reading ",data_filePro
            f_data = open(data_filePro , mode='rb')
            file_Notfinish=1
            while(file_Notfinish):
                f_header=get_frame_header(f_data)
                if len(f_header)==0:
                    file_Notfinish=0
                    break
                frame_size = int(f_header[0]/2)-2
                frame_rawData,frame_rawHeader,frame_all,time_stamp=get_frame(f_data,frame_size,0)
                time_all.append(time_stamp)
                allFrame.append(frame_all)
     
        fill_fre=0
        fill_num=0
        print 'length allFrame: ',len(allFrame)

        
        for index in range(len(allFrame)):
            frame_data_t=allFrame[index][16:].copy()
            for i in range(len(frame_data_t)):
                alldata.add_data("buffer",frame_data_t[i],i)
            fill_fre+=1
            if len(frames_perstep)==1 and fill_fre==int(frames_perstep[0]):
                print 'filling ',fill_num+1,' of ',Steps
                hitmap_m0=alldata.hitmap_t0
                hitmap_m1=alldata.hitmap_t1
                hitmap_m2=alldata.hitmap_t2
                Para_h.Fill(int(par[fill_num]))
                for i in range(nCols):
                    for j in range(nRows):
                        H_P0[fill_num].Fill(i,j,hitmap_m0[j][i])     
                        H_P1[fill_num].Fill(i,j,hitmap_m1[j][i])     
                        H_P2[fill_num].Fill(i,j,hitmap_m2[j][i])    
                        Hitmap_M0_3d.Fill(i,j,int(par[fill_num]),hitmap_m0[j][i]) 
                        Hitmap_M1_3d.Fill(i,j,int(par[fill_num]),hitmap_m1[j][i]) 
                        Hitmap_M2_3d.Fill(i,j,int(par[fill_num]),hitmap_m2[j][i])
                H_P0[fill_num].Write()
                H_P1[fill_num].Write()
                H_P2[fill_num].Write()
            
               # data_tree.Fill()
                alldata.__init__()
                fill_num+=1
                fill_fre = 0
            if len(frames_perstep)>1 and index==int(frames_perstep[fill_num+1]):
                print 'filling ',fill_num+1,' of ',Steps,' ',index,' frames'
                hitmap_m0=alldata.hitmap_t0
                hitmap_m1=alldata.hitmap_t1
                hitmap_m2=alldata.hitmap_t2
                Para_h.Fill(int(par[fill_num]))
                for i in range(nCols):
                    for j in range(nRows):
                        H_P0[fill_num].Fill(i,j,hitmap_m0[j][i])     
                        H_P1[fill_num].Fill(i,j,hitmap_m1[j][i])     
                        H_P2[fill_num].Fill(i,j,hitmap_m2[j][i])    
                        Hitmap_M0_3d.Fill(i,j,int(par[fill_num]),hitmap_m0[j][i]) 
                        Hitmap_M1_3d.Fill(i,j,int(par[fill_num]),hitmap_m1[j][i]) 
                        Hitmap_M2_3d.Fill(i,j,int(par[fill_num]),hitmap_m2[j][i]) 
                H_P0[fill_num].Write()
                H_P1[fill_num].Write()
                H_P2[fill_num].Write()
                # data_tree.Fill()
                alldata.__init__()
                fill_num+=1
        Hitmap_M0_3d.Write()
        Hitmap_M1_3d.Write()
        Hitmap_M2_3d.Write()
        Para_h.Write()
        #root_f.Write()
        root_f.Close()
    else:
        print("Can not find Data file! ")

def ReadConfigure(filename):
    f_s=open(filename)
    par=[]
    frames_perstep=[]
    changingRecording=False
    config_dic={}
    configureline=True
    debug=False

    for line in f_s.readlines():
        a=line.split()
        if '/u1/' not in a[0]:
            if configureline:
                if len(a)==1:
                    config_dic[a[0]]={}
                    key_a=a[0]
                if len(a)==2:
                    config_dic[key_a][a[0]]=a[1]
            if changingRecording:
                for i in a:
                    if i!='end':
                        b=str(i).split("=")
                        if len(b)==1:
                            par.append(b[0])
                        if len(b)==2:
                            par.append(b[0])
                            frames_perstep.append(b[1])     
                    else:
                        break 
            if 'Changing' in a[0]:
                print 'changing', a[1][:-1],' at ',a[2],' different values'
                Sweep_parameter=a[1][:-1] 
                Steps= a[2]
                configureline=False
            if 'Taking' in a[0]:
                print 'taking ', a[1],' for each value'
                frames_perstep.append(a[1])
                changingRecording=True
    if debug:
        for key in config_dic.keys():
            print key
            for i in config_dic[key]:
                print '\t',i,config_dic[key][i]
         
    return Sweep_parameter, Steps, frames_perstep, par, config_dic
        
def check_DataFileNumber(name_f):
    conf_filename=name_f+".txt"
    file_names=[]   
    if os.path.isfile(conf_filename):
        for i in range(1,100):
            d_fname=name_f+".dat."+str(i)
            if os.path.isfile(d_fname):
                file_names.append(d_fname)
            else:
                break
        if len(file_names)==0:
            print "Missing Data File"
    else:
        print "Missing Conf File"
    return conf_filename,file_names 


if True:
    data_ana(arg = sys.argv[1])
