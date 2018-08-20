#!/usr/bin/env python3
#-----------------------------------------------------------------------------
# Title      : PyRogue febBoard Module
#-----------------------------------------------------------------------------
# File       : febBoard.py
# Author     : Larry Ruckman <ruckman@slac.stanford.edu>
# Created    : 2016-11-09
# Last update: 2016-11-09
#-----------------------------------------------------------------------------
# Description:
# Rogue interface to FEB board
#-----------------------------------------------------------------------------
# This file is part of the ATLAS CHESS2 DEV. It is subject to 
# the license terms in the LICENSE.txt file found in the top-level directory 
# of this distribution and at: 
#    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
# No part of the ATLAS CHESS2 DEV, including this file, may be 
# copied, modified, propagated, or distributed except according to the terms 
# contained in the LICENSE.txt file.
#-----------------------------------------------------------------------------
import rogue.hardware.pgp
import rogue
import pyrogue.utilities.fileio
import pyrogue.gui
import pyrogue.protocols
import AtlasChess2Feb
import threading
import signal
import atexit
import yaml
import time
import sys
import os
import PyQt4.QtGui
import numpy as np
import datetime
import json
import csv
import random
import copyreg
from SCurveNP import *
from StreamReadout import *

READOUT_STR = 1 # 0: register reading 1: stream readout
MAKE_S_CURVE = True
QUIET_BOARD=False
c2_hists = []


##############################
# Set base
##############################
class System(pyrogue.Root):
    def __init__(self, guiTop, cmd, dataWriter, srp, **kwargs):
        super().__init__(name='System',description='Front End Board', **kwargs)
        #self.add(MyRunControl('runControl'))
        self.add(dataWriter)
        self.guiTop = guiTop

        @self.command()
        def Trigger():
            #cmd.sendCmd(0, 0)
            self._root.feb.sysReg.softTrig()

        # Add registers
        self.add(AtlasChess2Feb.feb(memBase=srp))

        # Add run cotnrol
        self.add(pyrogue.RunControl(name = 'runControl', description='Run Controller Chess 2', cmd=self.Trigger, rates={1:'1 Hz', 2:'2 Hz', 4:'4 Hz', 8:'8 Hz', 10:'10 Hz', 30:'30 Hz', 60:'60 Hz', 120:'120 Hz', 1000:'1000 Hz'}))


# Add data stream to file as channel 1 File writer
dataWriter = pyrogue.utilities.fileio.StreamWriter(name='dataWriter')
cmd = rogue.protocols.srp.Cmd()
# Create and Connect SRP to VC1 to send commands
srp = rogue.protocols.srp.SrpV3()



# Set base, make it visible for interactive mode
appTop = PyQt4.QtGui.QApplication(sys.argv)
guiTop = pyrogue.gui.GuiTop(group='PyRogueGui')
system = System(guiTop, cmd, dataWriter, srp)


def gui(arg = "192.168.4.28"):

    hists = []

    #################################################################
    # Check for PGP link
    if (arg == 'PGP'):
        # Create the PGP interfaces
        pgpVc0 = rogue.hardware.pgp.PgpCard('/dev/pgpcard_0',0,0) # Data
        pgpVc1 = rogue.hardware.pgp.PgpCard('/dev/pgpcard_0',0,1) # Registers

        # Display PGP card's firmware version
        print("")
        print("PGP Card Version: %x" % (pgpVc0.getInfo().version))
        print("")
        #connect commands to  VC0
        pyrogue.streamConnect(cmd, pgpVc0)

        # Create and Connect SRPv0 to VC1
        ##srp = rogue.protocols.srp.SrpV0()
        pyrogue.streamConnectBiDir(pgpVc1,srp)
        
        # Add data stream to file as channel 1
        pyrogue.streamConnect(pgpVc0,dataWriter.getChannel(0x1))
    #################################################################
    # Else it's Ethernet based
    else:
        # Create the ETH interface @ IP Address = arg
        ethLink = pyrogue.protocols.UdpRssiPack(host=arg,port=8192,size=1400)    
    
        #connect commands to  VC0
        pyrogue.streamConnect(cmd, ethLink.application(0))
        # Create and Connect SRPv0 to AxiStream.tDest = 0x0
        ##srp = rogue.protocols.srp.SrpV0()  
        pyrogue.streamConnectBiDir(srp,ethLink.application(0))

        # Add data stream to file as channel 1 to tDest = 0x1
        pyrogue.streamConnect(ethLink.application(1),dataWriter.getChannel(0x1))
    #################################################################
             
    system.start(pollEn=True, pyroGroup=None, pyroHost=None)
    guiTop.addTree(system)
    guiTop.resize(800,1000)
   
    log_file="log_all.log"
    log_f = open(log_file,"a")
    description = input("Describe the test:\n")
    path_l="configure_log.txt"
    l_file = open(path_l,"w")
    save_configureFile(l_file,"../config/defaultR2_test.yml"); 
    system.root.ReadConfig("../config/defaultR2_test.yml")
    print("- Loading config file....")
    #time1=datetime.datetime.now()
    time1=time.time()
    if (READOUT_STR==1):
        hotpixel_m0=[]
        hotpixel_m1=[]
        hotpixel_m2=[(123,20)]
        print("- Stream readout mode -")
        Nframes = 1000
        Trigger_type = [-1,1000] # -1: softTrigger, others: to be determined(LEMO trigger for now)
        Pixels = None
        Parameter_interested=['TH']
        #P_range=range(0x400, 0x410, 0x6)
        P_range=range(0x258, 0x4b0, 0x6)
        Path=""
        s_name=StreamRO_concept(system, Nframes, Trigger_type, Pixels, Parameter_interested, P_range, Path, l_file, hotpixel_m0, hotpixel_m1, hotpixel_m2) 
        log_f.write() 
        l_file.close()
        os.rename(path_l,s_name+'.txt')
        #time2=datetime.datetime.now()
        log_f.write(s_name+" :\n")
        log_f.write("--- "+description+"\n")
        log_f.close()
        print("finished in "+str(time2-time1)+" seconds")


    if (MAKE_S_CURVE and READOUT_STR==0):
        simu=False
        run = 'test1'  
        Qinj = [1,0]
        a1='01'
        reading_all_together=True
        Dump_event=False
        real_time=1 # 0--turn off real-time figure 1: on 
        BL_value=[0x2e8] #BL=0.6v
        values = [6]
        #values = [6]#, 5, 4, 3, 2, 1, 0, 7, 8, 9]
        a=sys.argv[1]
        InvPulse=False
        #PulseDelay=0x18ff #20000ns
        #PulseDelay=0xc7f #10000ns
        PulseDelay=0x0 #3.15ns
        #PulseDelay=0x3e7f #50000ns
        #PulseDelay=0x63ff #80000ns
        PulseWidth=0x12bf  #15000ns
        system.feb.chargeInj.pulseWidthRaw.set(PulseWidth)
        #system.feb.chargeInj.pulseDelayRaw.set(0xc7f) #10000ns`
        system.feb.chargeInj.pulseDelayRaw.set(PulseDelay)
        system.feb.chargeInj.invPulse.set(InvPulse) 
        print(a1)
        print("logging...")
        logfile("chess2_scan_SCurveTest_"+today1+"_board_"+str(sys.argv[1])+"_run_" + str(run)+".log")
        for value in values:
            logging.info('Running the test with Values='+str(value))
            for chargeInjectionEnbled in Qinj:
                logging.info("Using board: "+str(sys.argv[1]))
                deltaBLToBLR = value * 120 
                thresholds =range(0x3e1, 0x3ee, 0x1) #0.7
                pixels=[(62,19)]
                if 1:
                    #if pixels!=None:
                    #    print("    Testing Pixel: "+str(pixels))
                        #logging.info("    Testing Pixel: "+str(pixels))
                        #logging.info("    Testing Pixel "+str(pixels))
                    #for pixel_i in pixels:
                    if 1:
                       # pixel_j=[(pixel_i[0],pixel_i[1])]
                       # print("testing on pixel: "+str(pixel_i))
                        for BL_value_i in BL_value:
                            hists = makeCalibCurve4( system, nCounts=100, thresholdCuts = thresholds, pixels=pixels, histFileName="scurve_test_sleep.root", deltaBLToBLR = deltaBLToBLR, chargeInjectionEnbled = chargeInjectionEnbled, BL=BL_value_i,Reading_all_pixel_together=reading_all_together,mode=real_time)
                           # create file header
                            headerText = "\n# raw data of tests"
                            headerText = headerText + "\n# pixels, " + str(pixels)
                            headerText = headerText + "\n# chargeInjectionEnbled, " + str(chargeInjectionEnbled)
                            headerText = headerText + "\n# deltaBLToBLR:," + str(deltaBLToBLR) 
                            headerText = headerText + "\n# system.feb.dac.dacBLRaw:," + str(system.feb.dac.dacBLRaw.get()) 
                            headerText = headerText + "\n# trim, " + str(7)
                            headerText = headerText + "\n# thresholds (raw):," + str(thresholds)
                            headerText = headerText + "\n# PulseDelay:"+str(PulseDelay)
                            headerText = headerText + "\n# PulseWidth:"+str(PulseWidth)
                            headerText = headerText + "\n# invPulse:"+str(InvPulse)

                            save_name="/chess2_scan_SCurveTest_"+today1+"_board_"+str(sys.argv[1])+"_run_" +str(run)+"_BL_"+str(BL_value_i)+"_chargeInjectionEnbled_"+ str(chargeInjectionEnbled) + "_thN_"
                        save_f_json(save_name,hists)
                        logging.info(headerText)
                    
    
    if (QUIET_BOARD):
        system.feb.chargeInj.calPulseInh.set(1)
        print("Disable all pixels")
        trim=7
        system.feb.Chess2Ctrl0.writeAllPixels(enable= 0,chargeInj= 1,trimI= trim)
        system.feb.Chess2Ctrl1.writeAllPixels(enable= 0,chargeInj= 1,trimI= trim)
        system.feb.Chess2Ctrl2.writeAllPixels(enable= 0,chargeInj= 1,trimI= trim)
    

    # Run gui
    appTop.exec_()

    # Stop mesh after gui exits
    system.stop()
    
    return hists

if __name__ == '__main__':
    rogue.Logging.setFilter('pyrogue.SrpV3', rogue.Logging.Debug)
    c2_hists = gui(arg = sys.argv[1])
   
