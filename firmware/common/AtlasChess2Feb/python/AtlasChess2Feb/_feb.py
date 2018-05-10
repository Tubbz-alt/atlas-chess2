#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : PyRogue feb Module
#-----------------------------------------------------------------------------
# File       : feb.py
# Author     : Larry Ruckman <ruckman@slac.stanford.edu>
# Created    : 2016-11-09
# Last update: 2016-11-09
#-----------------------------------------------------------------------------
# Description:
# PyRogue feb Module
#-----------------------------------------------------------------------------
# This file is part of the ATLAS CHESS2 DEV. It is subject to 
# the license terms in the LICENSE.txt file found in the top-level directory 
# of this distribution and at: 
#    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
# No part of the ATLAS CHESS2 DEV, including this file, may be 
# copied, modified, propagated, or distributed except according to the terms 
# contained in the LICENSE.txt file.
#-----------------------------------------------------------------------------

import pyrogue as pr

import surf
import surf.axi as axi
import surf.xilinx as xilinx
import AtlasChess2Feb

class feb(pr.Device):
    def __init__(self, **kwargs):

        if 'description' not in kwargs:
            kwargs['description'] = "HR Gen1 FPGA"

        super(self.__class__, self).__init__(**kwargs)
        ######################################
        # SACI base address and address stride 
        ######################################
        saciAddr = 0x01000000
        saciChip = 0x400000        
        
        #############
        # Add devices
        #############
        self.add(axi.AxiVersion(                            offset=0x00000000,expand=False))
        self.add(xilinx.Xadc(                               offset=0x00010000,expand=False))  
        self.add(AtlasChess2Feb.sysReg(   name="sysReg",    offset=0x00030000,expand=False))    
        self.add(AtlasChess2Feb.memReg(   name="memReg",    offset=0x00040000,expand=True))    
        #self.add(AtlasChess2Feb.iobuff(   name="iobuff",    offset=0x00500000,expand=False))    
        self.add(AtlasChess2Feb.dac(      name="dac",       offset=0x00100000,expand=False))                
        self.add(AtlasChess2Feb.chargeInj(name="chargeInj", offset=0x00330000,expand=False))   
                
        for i in range(3):
            self.add(AtlasChess2Feb.Chess2Array( 
                name='Chess2Ctrl%01i'%(i),
                offset=(saciAddr + i*saciChip),enabled=False,expand=False))   
                
        self.add(AtlasChess2Feb.Chess2Test(name="Chess2Test", offset=saciAddr+(3*saciChip),enabled=False,expand=False))
        
