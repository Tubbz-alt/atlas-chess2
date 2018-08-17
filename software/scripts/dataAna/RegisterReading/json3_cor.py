#from __future__ import pickle
import pickle
import csv
import json
from ROOT import *
from ROOT import gROOT, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TLorentzVector, TGraphErrors, TGraph
from ROOT import TPad, TPaveText, TLegend, THStack
from ROOT import gBenchmark, gStyle, gROOT, gPad
import sys
import re
from array import array
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from SCurveNP import *
#gROOT.SetStyle("Plain")   # set plain TStyle
#gStyle.SetOptStat(0);
#gROOT.SetBatch(1)         #This was to suppress the canvas outputs
#gStyle.SetOptStat(111111) # draw statistics on plots,
                            # (0) for no output
#gStyle.SetPadTickY(1)
#gStyle.SetOptFit(1111)    # draw fit results on plot,
                            # (0) for no ouput
#gStyle.SetPalette(57)     # set color map
#gStyle.SetOptTitle(0)     # suppress title box
#def plot(csv_file,projection=1): 
class timep:
    def __init__(self,pixel1,matrix1,index1,threshold1,time1):
        self.pixel=pixel1
        self.matrix=matrix1
        self.index=index1
        self.threshold=threshold1
        self.time=time1

def dic2timep(dic):
    return timep(dic['pixel'],dic['matrix'],dic['index'],dic['threshold'],dic['time'])

def plot(name_f_json,projection=1):    
    ncol=32
    nrow=128
    sweep_type='threshold'
    time_scale=200000
    # one for each ASIC
    #pixels=[(0,1)]
    pixels,thresholdCuts=get_pixelsandthresholds(name_f_json+'.json')
    
    if len(pixels)>10:
        enable_all_pixel=True
        print(len(pixels))
    else: enable_all_pixel=False
    matrix=[0,1,2]
    hits=(0,1,2,3,4,5,6,7)
    data_dic={}
    #pulse_end=pulse_start+pulse_width
    fast_range=1500
    with open(name_f_json+'.json') as f:
    #with open('f_j.json') as f:
        hist=json.load(f,object_hook=dic2timep)
        data_dic=get_allHists(pixels,matrix,hits,thresholdCuts)
        #data_dic=get_allHists(pixels,matrix,thresholdCuts,hits)
        for a in hist:
            p1=a.pixel[0]
            p2=a.pixel[1]
            data_dic[(p1,p2)][a.matrix][a.index][a.threshold]=a.time
    if (not enable_all_pixel): 
        rootf = TFile(name_f_json+'.root',"RECREATE")
        #rootf = TFile(name_f_json+'_nofastn.root',"RECREATE")
        for key in data_dic: #pixel
            print(key)
            for key1 in data_dic[key]: #matrix
                h="hitnumber_pixel_"+str(key)+"_asic"+str(key1)+"_THsweep"
                h=TH1D(h,";Hit;Hits number",8,0,8)  
                h_name_all="cumulTimeHist_pixel_"+str(key)+"_asic"+str(key1)+"_THsweep"
                #h_name_g="cumulTimeHist_pixel_"+str(key)+"_asic"+str(key1)+"_THsweep_g"
                a=[]
                for key3 in data_dic[key][key1][1]: #threshold
                    a.append(key3)
                a1=[float(b)/1241. for b in a]
                hist_name_all=TH2D(h_name_all,";Threshold [V];Time [ns]", len(thresholdCuts), min(a1), max(a1), 2000, 0, time_scale)
                h_t0="cumulTimeHist_pixel_"+str(key)+"_asic"+str(key1)+"_THsweep_time0"
                h_t0=TH1D(h_t0,";Threshold [V];Hits number",len(thresholdCuts), min(a1), max(a1))  
                #hist_name_all=TH2D(h_name_all,";Threshold [V];Time [ns]", (th_h-th_l)/th_delta, min(a1), max(a1), 2000, 0, time_scale)
                for key2 in data_dic[key][key1]:  #index
                    
                    h_name="cumulTimeHist_pixel_"+str(key)+"_asic"+str(key1)+"_hit_"+str(key2)+"_THsweep"
                    hist_name=TH2D(h_name,";Threshold [V];Time [ns]", len(thresholdCuts), min(a1), max(a1), 800, 0, time_scale)
                    g_x=[]
                    g_y=[]
                    g_ex=[]
                    g_ey=[]
                    a=data_dic[key][key1][key2].keys()
                    a.sort()
                    for key3 in a: #threhsold
                    #for key3 in data_dic[key][key1][key2]: #threhsold
                        t_aftercut=[]
                        for val_i in range(len(data_dic[key][key1][key2][key3])):
                            timev=data_dic[key][key1][key2][key3][val_i]
                            if timev<=time_scale:
                                if timev==-2.0:
                                    h_t0.Fill(float(key3)/1241)
                                if timev>0:
                                #if (timev<35000):
                                #if timev>1000:
                                    t_aftercut.append(timev)
                                    hist_name.Fill(float(key3)/1241,timev)
                                    hist_name_all.Fill(float(key3)/1241,timev)
                                    h.Fill(key2)
                        if len(t_aftercut)!=0:
                            t_aftercut_a=np.array(t_aftercut)
                            g_x.append(float(key3)/1241)
                            #print(float(key3)/1241)
                            g_y.append(np.mean(t_aftercut_a))
                            g_ey.append(np.std(t_aftercut_a))
                            g_ex.append(0)
                    hist_name.Write()
                    g_ax=np.array(g_x)
                    g_ay=np.array(g_y)
                    g_aex=np.array(g_ex)
                    g_aey=np.array(g_ey)
                    
                    #hist_name_g=TGraph(len(g_ax),g_ax,g_ay)
#                    #hist_name_g="cumulTimeHist_pixel_"+str(key)+"_asic"+str(key1)+"_hit_"+str(key2)+"_THsweep_g"
                    if len(g_ax)!=0:
                        graph_g=TGraph(len(g_ax),g_ax,g_ay)
                        graph_g.SetName("cumulTimeHist_pixel_"+str(key)+"_asic"+str(key1)+"_hit_"+str(key2)+"_THsweep_graph")
                        graph_g.SetTitle(";Threshold [V];Time [ns]")
                        graph_g.SetMarkerStyle(20);
                        graph_g.SetMarkerSize(0.6);
                        graph_g.Write()
                        hist_name_g=TGraphErrors(len(g_ax),g_ax,g_ay,g_aex,g_aey)
                        hist_name_g.SetName("cumulTimeHist_pixel_"+str(key)+"_asic"+str(key1)+"_hit_"+str(key2)+"_THsweep_g")
                        hist_name_g.SetTitle(";Threshold [V];Time [ns]")
                        hist_name_g.SetFillColor(1);
                        hist_name_g.SetMarkerStyle(20);
                        hist_name_g.SetMarkerSize(0.6);
                        hist_name_g.Write()
                    if projection:
                        cut1=[min(a1),0]
                        cut2=[max(a1),time_scale]
                        proj_x=get_proj_X(hist_name,h_name,cut1,cut2,min(a1),max(a1))
                        proj_y=get_proj_Y(hist_name,h_name,cut1,cut2,0,time_scale)
                        proj_x.Write()
                        proj_y.Write()
                    #hist_name_g="cumulTimeHist_pixel_"+str(key)+"_asic"+str(key1)+"_THsweep_g"
                    #hist_name_g=TGraphErrors(n,g_ax,g_aex,g_ay,g_aey)
                    #hist_name_g=TGraphErrors(n,g_ax,g_aex,g_ay,g_aey)
                    #hist_name_g.SetTitle("cumulTimeHist_pixel_"+str(key)+"_asic"+str(key1)+"_THsweep_g")
                    #hist_name_g=TGraphErrors(h_name_g,";Threshold [V];Time [ns]",n,g_x,g_y,g_ex,g_ey)
                hist_name_all.Write()
                h_t0.Write()
                h.Write()
                if projection:
                    cut1=[min(a1),0]
                    cut2=[max(a1),140000]
                    proj_x_all=get_proj_X(hist_name_all,h_name_all,cut1,cut2,min(a1),max(a1))
                    proj_y_all=get_proj_Y(hist_name_all,h_name_all,cut1,cut2,0,time_scale)
                    proj_x_all.Write()
                    proj_y_all.Write()
                
        rootf.Close()     
    else:
        for i_k in range(0,2,1):
            hitmap_name={0:{0:"chess2_matrix0_hit_0",1:"chess2_matrix0_hit_1",2:"chess2_matrix0_hit_2",3:"chess2_matrix0_hit_3",4:"chess2_matrix0_hit_4",5:"chess2_matrix0_hit_5",6:"chess2_matrix0_hit_6",7:"chess2_matrix0_hit_7",8:"chess2_matrix0_allhit"},1:{0:"chess2_matrix1_hit_0",1:"chess2_matrix1_hit_1",2:"chess2_matrix1_hit_2",3:"chess2_matrix1_hit_3",4:"chess2_matrix1_hit_4",5:"chess2_matrix1_hit_5",6:"chess2_matrix1_hit_6",7:"chess2_matrix1_hit_7",8:"chess2_matrix1_allhit"},2:{0:"chess2_matrix2_hit_0",1:"chess2_matrix2_hit_1",2:"chess2_matrix2_hit_2",3:"chess2_matrix2_hit_3",4:"chess2_matrix2_hit_4",5:"chess2_matrix2_hit_5",6:"chess2_matrix2_hit_6",7:"chess2_matrix2_hit_7",8:"chess2_matrix2_allhit"},}
            histt_name={0:{0:"chess2_matrix0_hit_0_t",1:"chess2_matrix0_hit_1_t",2:"chess2_matrix0_hit_2_t",3:"chess2_matrix0_hit_3_t",4:"chess2_matrix0_hit_4_t",5:"chess2_matrix0_hit_5_t",6:"chess2_matrix0_hit_6_t",7:"chess2_matrix0_hit_7_t",8:"chess2_matrix0_allhit_t"},1:{0:"chess2_matrix1_hit_0_t",1:"chess2_matrix1_hit_1_t",2:"chess2_matrix1_hit_2_t",3:"chess2_matrix1_hit_3_t",4:"chess2_matrix1_hit_4_t",5:"chess2_matrix1_hit_5_t",6:"chess2_matrix1_hit_6_t",7:"chess2_matrix1_hit_7_t",8:"chess2_matrix1_allhit_t"},2:{0:"chess2_matrix2_hit_0_t",1:"chess2_matrix2_hit_1_t",2:"chess2_matrix2_hit_2_t",3:"chess2_matrix2_hit_3_t",4:"chess2_matrix2_hit_4_t",5:"chess2_matrix2_hit_5_t",6:"chess2_matrix2_hit_6_t",7:"chess2_matrix2_hit_7_t",8:"chess2_matrix2_allhit_t"},}
            dataq_name={0:{0:"chess2_matrix0_hit_0_DataDistribution",1:"chess2_matrix0_hit_1_DataDistribution",2:"chess2_matrix0_hit_2_DataDistribution",3:"chess2_matrix0_hit_3_DataDistribution",4:"chess2_matrix0_hit_4_DataDistribution",5:"chess2_matrix0_hit_5_DataDistribution",6:"chess2_matrix0_hit_6_DataDistribution",7:"chess2_matrix0_hit_7_DataDistribution",8:"chess2_matrix0_allhit_DataDistribution"},1:{0:"chess2_matrix1_hit_0_DataDistribution",1:"chess2_matrix1_hit_1_DataDistribution",2:"chess2_matrix1_hit_2_DataDistribution",3:"chess2_matrix1_hit_3_DataDistribution",4:"chess2_matrix1_hit_4_DataDistribution",5:"chess2_matrix1_hit_5_DataDistribution",6:"chess2_matrix1_hit_6_DataDistribution",7:"chess2_matrix1_hit_7_DataDistribution",8:"chess2_matrix1_allhit_DataDistribution"},2:{0:"chess2_matrix2_hit_0_DataDistribution",1:"chess2_matrix2_hit_1_DataDistribution",2:"chess2_matrix2_hit_2_DataDistribution",3:"chess2_matrix2_hit_3_DataDistribution",4:"chess2_matrix2_hit_4_DataDistribution",5:"chess2_matrix2_hit_5_DataDistribution",6:"chess2_matrix2_hit_6_DataDistribution",7:"chess2_matrix2_hit_7_DataDistribution",8:"chess2_matrix2_allhit_DataDistribution"},}
            print("generating hitmap.....")
            if i_k==0:
                rootf = TFile(name_f_json+'_AllPixelsEnabled_cor.root',"RECREATE")
            else: 
                rootf = TFile(name_f_json+'_AllPixelsEnabled_timecut_cor.root',"RECREATE")
            data_type_name=["-1.0","-2.0","Time data"]
            for map_key in hitmap_name:
                for map_key1 in hitmap_name[map_key]:
                    hitmap_name[map_key][map_key1]=TH2D(hitmap_name[map_key][map_key1],";Row;Col", ncol, 0, ncol, nrow, 0, nrow)
                    histt_name[map_key][map_key1]=TH1D(histt_name[map_key][map_key1],";Time [ns];Hit_number", 800, 0, time_scale)
                   # dataq_name[map_key][map_key1]=TH1D(dataq_name[map_key][map_key1],";Data type;Number", 3, 0, 3)
            for a_i in hist:
                for time_1 in a_i.time:
                  #  if time_1==-1.0:
                  #      dataq_name[a_i.matrix][a_i.index].Fill(0)
                  #      dataq_name[a_i.matrix][8].Fill(0)
                  #  if time_1==-2.0:
                  #      dataq_name[a_i.matrix][a_i.index].Fill(1)
                  #      dataq_name[a_i.matrix][8].Fill(1)
                    if i_k==0 and time_1>0:
                    #if 50000<time_1:
                        hitmap_name[a_i.matrix][a_i.index].Fill(a_i.pixel[1],a_i.pixel[0])
                        hitmap_name[a_i.matrix][8].Fill(a_i.pixel[1],a_i.pixel[0])
                        histt_name[a_i.matrix][a_i.index].Fill(time_1)
                        histt_name[a_i.matrix][8].Fill(time_1)
                    if i_k==1 and 3500<time_1:
                        hitmap_name[a_i.matrix][a_i.index].Fill(a_i.pixel[1],a_i.pixel[0])
                        hitmap_name[a_i.matrix][8].Fill(a_i.pixel[1],a_i.pixel[0])
                        histt_name[a_i.matrix][a_i.index].Fill(time_1)
                        histt_name[a_i.matrix][8].Fill(time_1)
                  #      dataq_name[a_i.matrix][a_i.index].Fill(2)
                  #      dataq_name[a_i.matrix][8].Fill(2)
            for map_key in hitmap_name:
                for map_key1 in hitmap_name[map_key]:
                    hitmap_name[map_key][map_key1].Write()
                    histt_name[map_key][map_key1].Write()
                  #  dataq_name[map_key][map_key1].Write()
                   # dataq_name[map_key][map_key1].SetStats(0)
                  #  for i in range(1,4):
                  #     dataq_name[map_key][map_key1].GetXaxis().SetBinLabel(i,data_type_name[i-1])

            rootf.Close()
            print 'Done!'
         
                
                
def cut_area(cut_point1,cut_point2,x_name='threshold',y_name='time'):
    cut=TCutG("cut",4)
    cut.SetVarX(x_name)
    cut.SetVarY(y_name)
    cut.SetPoint(0,cut_point1[0],cut_point1[1])
    cut.SetPoint(1,cut_point1[0],cut_point2[1])
    cut.SetPoint(2,cut_point2[0],cut_point2[1])
    cut.SetPoint(3,cut_point2[0],cut_point1[1])
    return cut

def get_proj_X(hist_name,file_name,cut1,cut2,minx,maxx):
    p_name=str(file_name)+"projection_on_threshold"
    proj_x=TH1D("proj_x","projection on threshold",1000,minx,maxx)
    cut=cut_area(cut1,cut2)
    proj_x=hist_name.ProjectionX("_px",0,-1,"[cut]")
    #proj_x=hist_name.ProjectionX(hist_name,Ycut1,Ycut2)
    return proj_x 

def get_proj_Y(hist_name,file_name,cut1,cut2,miny,maxy):
    p_name=str(file_name)+"projection_on_time"
    proj_y=TH1D("proj_y","projection on time",1000,miny,maxy)
    cut=cut_area(cut1,cut2)
    proj_y=hist_name.ProjectionY("_py",0,-1,"[cut]") 
    #proj_y=hist_name.ProjectionY(hist_name,Xcut1,Xcut2) 
    return proj_y

def file_name(file_dir='/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02',file_h='None'):
    if file_h=="None":
        print("no file selected!")
    else:
        L=[]
        for root,dirs,files in os.walk(file_dir):
            for file_i in files:
                #if os.path.splitext(file)[1]=='':
                if os.path.splitext(file_i)[0][0:-3]==file_h:
                    print(file_i)
                    L.append(file_i)
                if os.path.splitext(file_i)[0]==file_h:
                    L.append(file_i)
                    print(file_i)
    print 'Number of files: ',len(L)
    return L
#file_name(file_h='chess2_scan_SCurveTest_04122018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v_3')
#chess2_scan_SCurveTest_04122018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v_3
#for bl in [8,310,434,576]:
#for bl in [930,1365]:
for bl in [744]:
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-19/chess2_scan_SCurveTest_02262018_board_192.168.3.28_run_N10_BL_"+str(bl)+"_chargeInjectionEnbled_0_thN_0x6withbias12_(60,13)_PXTHsweep_hitmap_50000ns_detail2",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-19/chess2_scan_SCurveTest_02262018_board_192.168.3.28_run_N10_BL_"+str(bl)+"_chargeInjectionEnbled_1_thN_0x6withbias12_(60,13)_PXTHsweep_hitmap_50000ns_detail2",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-19/chess2_scan_SCurveTest_03222018_board_192.168.3.28_run_N14_BL_744_chargeInjectionEnbled_1_thN_0x6withbias4V_withlaser_PXTHsweep",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-19/chess2_scan_SCurveTest_03232018_board_192.168.3.28_run_N14_BL_744_chargeInjectionEnbled_1_thN_0x6withbias_PXTHsweep_hitmap_1.1",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-19/chess2_scan_SCurveTest_03222018_board_192.168.3.28_run_N14_BL_744_chargeInjectionEnbled_0_thN_0x6withbias4V_withlaser_PXTHsweep",1)
#    plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_04112018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v",1)
    plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-01/chess2_scan_SCurveTest_05212018_board_192.168.3.28_run_test_BL_744_chargeInjectionEnbled_0_thN_0x6_Bias_-7_M1_1P_thscan",1)
  #  plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-01/chess2_scan_SCurveTest_05212018_board_192.168.3.28_run_test_BL_744_chargeInjectionEnbled_1_thN_0x6_Bias_-7_M1_1P_thscan",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-19/chess2_scan_SCurveTest_04032018_board_192.168.3.28_run_N16_BL_1280_chargeInjectionEnbled_1_thN_0x6_pos3_05_PXTHsweep",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-19/chess2_scan_SCurveTest_04032018_board_192.168.3.28_run_N16_BL_1280_chargeInjectionEnbled_1_thN_0x6_pos4_PXTHsweep",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-19/chess2_scan_SCurveTest_03272018_board_192.168.3.28_run_N15_BL_744_chargeInjectionEnbled_0_thN_0x6withbias12_(52,31)_5v_6vcooling",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-28/chess2_scan_SCurveTest_02072018_board_192.168.3.28_run_N8_BL_"+str(bl)+"_chargeInjectionEnbled_1_thN_0x6withbias8_PXTHsweep_hitmap_th1.3_no00_cooling6v",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-28/chess2_scan_SCurveTest_02072018_board_192.168.3.28_run_N8_BL_"+str(bl)+"_chargeInjectionEnbled_0_thN_0x6withbias8_PXTHsweep_hitmap_th1.1_no00_cooling6v",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-28/chess2_scan_SCurveTest_02042018_board_192.168.3.28_run_N7_BL_"+str(bl)+"_chargeInjectionEnbled_1_thN_0x6withbias4_PXTHsweep_narrow",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_01302018_board_192.168.3.28_run_N3_BL_"+str(bl)+"_chargeInjectionEnbled_0_thN_0x6withbias8_PXTHsweep_led_30000ns",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_02022018_board_192.168.3.28_run_N4_BL_"+str(bl)+"_chargeInjectionEnbled_1_thN_0x6withbias8_PXTHsweep_narrow",1)
    #plot("/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_02022018_board_192.168.3.28_run_N4_BL_"+str(bl)+"_chargeInjectionEnbled_0_thN_0x6withbias8_PXTHsweep_narrow",1)
     
