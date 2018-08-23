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
import PyQt4.QtGui
import numpy as np
import datetime
import json
import csv
import random
import copyreg

from System import System
from EventReader import EventReader
from ScanTest import ScanTest
from Hist_Plotter import Hist_Plotter
from Frame_data import *
from Hitmap_Plotter import Hitmap_Plotter
from ChessControl import ChessControl
np.set_printoptions(threshold=np.inf)

# Add data stream to file as channel 1 File writer
dataWriter = pyrogue.utilities.fileio.StreamWriter(name='dataWriter')
cmd = rogue.protocols.srp.Cmd()
# Create and Connect SRP to VC1 to send commands
srp = rogue.protocols.srp.SrpV3()

# Set base, make it visible for interactive mode
appTop = PyQt4.QtGui.QApplication(sys.argv)
guiTop = pyrogue.gui.GuiTop(group='PyRogueGui')
system = System(guiTop, cmd, dataWriter, srp)
chess_control = ChessControl(system)
eventReader = EventReader(chess_control)

def init_best_vals():
    best_vals = {}
    best_vals["Chess2Ctrl1.VPFBatt"] = 0xa
    best_vals["Chess2Ctrl1.VNLogicatt"] = 0x1c
    best_vals["Chess2Ctrl1.VNSFatt"] = 0x1d
    best_vals["Chess2Ctrl1.VNatt"] = 0x1e
    best_vals["Chess2Ctrl1.VPLoadatt"] = 0x1e
    best_vals["Chess2Ctrl1.VPTrimatt"] = 0xc #not very important--see 08-03_17-47
    return best_vals

def gui(ip = "192.168.2.101", configFile = "../config/defaultR2_test.yml" ):

    #################################################################
    # Check for PGP link
    if (ip == 'PGP'):
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
        #srp = rogue.protocols.srp.SrpV0()
        pyrogue.streamConnectBiDir(pgpVc1,srp)
        
        # Add data stream to file as channel 1
        pyrogue.streamConnect(pgpVc0,dataWriter.getChannel(0x1))

    else: # Else it's Ethernet based
        # Create the ETH interface @ IP Address = ip
        ethLink = pyrogue.protocols.UdpRssiPack(host=ip,port=8192,size=1400)    
    
        #connect commands to  VC0
        pyrogue.streamConnect(cmd, ethLink.application(0))
        # Create and Connect SRPv0 to AxiStream.tDest = 0x0
        pyrogue.streamConnectBiDir(srp,ethLink.application(0))

        # Add data stream to file as channel 1 to tDest = 0x1
        pyrogue.streamConnect(ethLink.application(1),eventReader)

        #old version in below 2 lines
        #fileReader = dataWriter.getChannel(0x1)
        #pyrogue.streamConnect(ethLink.application(1),dataWriter.getChannel(0x1))
    chess_control.start()
    guiTop.addTree(chess_control.system)
    guiTop.resize(800,1000)
    chess_control.read_config(configFile)
    print("Loading config file")

    """ Performs a test on a 8x1 block of pixels """

    #TODO check that pktWordSize is the nb of 64b frame received
    chess_control.set_pktWordSize(255)

    fields = ["Chess2Ctrl1."+x for x in ["VPTrimatt","VPLoadatt","VNatt","VNSFatt","VNLogicatt","VPFBatt"]]
    best_vals = init_best_vals()
    specials = ["dac.dacPIXTHRaw","dac.dacBLRaw"]
    #scan_fields = ["dac.dacPIXTHRaw","dac.dacBLRaw","Chess2Ctrl1.VPTrimatt"]
    scan_fields = ["dac.dacBLRaw"]
    
    param_config_info_const = "" #never changes after this init
    val_ranges = {} #range of values to scan a given parameter key
    #init val_ranges and param_config_info_const
    for f in fields:
        val_ranges[f] = range(0,32)
        param_config_info_const += f+"="+str(best_vals[f])+","
    for sp in specials:
        #val_ranges[sp] = range(900,1400,100) #threshold or baseline
        val_ranges[sp] = [0x2e8]*5 #keep special val fixed
   	#[0x2e8,0x2e8,...] 

    sleeptime = 2000 #ms
    runrate = 1000 #Hz
    
    threshold_xrange = range(int(600*4096/3300),int(1000*4096/3300),4) #used when scanning bl or any param
    baseline_xrange = range(0,1000,8) #only used when scanning through thresholds

    #Loop through scan_fields, scan given range of values for that scan_field. 
    # Each value of scan_field makes a plot.
    for scan_field in scan_fields:
        param_config_info_tmp = "" #changes for each config file
        for sf in scan_fields:
            if sf != scan_field and sf not in specials:
                param_config_info_tmp += sf+"="+str(best_vals[sf])+","
        param_config_info = param_config_info_const + param_config_info_tmp

        #disable all pixels
        print("Disable all pixels")
        chess_control.disable_all_pixels(all_matrices=True)
        #disable data stream
        chess_control.close_stream() #opened in scan_test.scan()...	

        scan_test = ScanTest()
        scan_test.set_matrix(1)
        scan_test.set_scan_field(scan_field)
    	#--> scanning system.feb.Chess2Ctrl1.<val_field>
        scan_test.set_scan_range(val_ranges[scan_field])
        
        #scan_test.set_shape((8,1)) #block of 8 rows by 1 column
        scan_test.set_shape((1,1))
        
        #scan_test.set_topleft((112,31)) #128 rows,32 cols
        scan_test.set_topleft((62,19))
        #sleeptime = 1000/336*1000 #ms
        scan_test.set_sleeptime(sleeptime) #ms,controls how many frames collected
        chess_control.set_run_rate(runrate) #trigger rate is 1000Hz
        scan_test.set_pulserStatus("OFF") #just to inform filename
        scan_test.set_chargeInjEnabled(1) #1 is enabled, 0 prevents chargeInj's
        if scan_test.chargeInjEnabled:
            scan_test.init_chargeInj(chess_control,
                                pulse_width=15000,
                                pulse_delay=0,
                                inv_pulse=False, #sends a negative pulse
                                inh_pulse=False) #can inhibit pulse
        print("Enabling block")
        scan_test.enable_block(chess_control)

        if scan_field == "dac.dacBLRaw":
            scan_test.set_scan_type("baseline_scan")
            scan_test.set_x_vals(threshold_xrange)
        elif scan_field == "dac.dacPIXTHRaw":
            scan_test.set_scan_type("threshold_scan")
            scan_test.set_x_vals(baseline_xrange)
        else: #make default x_values thresholds for now
            scan_test.set_scan_type("other_scan")
            scan_test.set_x_vals(threshold_xrange)
            scan_test.set_fixed_baseline(744) #arbitrary (0,2000)

        eventReader.hitmap_show()
        #controlled scan through each val while keeping all other vals at configuration values
        for scan_field in scan_fields:
            if scan_field not in specials:
                chess_control.set_val(scan_field,best_vals[scan_field])
        scan_test.scan(chess_control,eventReader,param_config_info,runrate)

    # Run gui
    appTop.exec_()

    # Stop mesh after gui exits
    chess_control.stop()
    

if __name__ == '__main__':
    rogue.Logging.setFilter('pyrogue.SrpV3', rogue.Logging.Debug)
    if len(sys.argv) == 1:
        gui()
    elif len(sys.argv) == 3:
        #allow ip and configFile to be overwritten via commandline args
        gui(ip = sys.argv[1],configFile = sys.argv[2]) 
    else:
        raise("USAGE: python3 FebScriptTest.py <board ip> <configFile>")
