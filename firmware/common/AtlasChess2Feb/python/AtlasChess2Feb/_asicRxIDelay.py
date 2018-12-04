#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : PyRogue _chargeInj Module
#-----------------------------------------------------------------------------
# File       : _chargeInj.py
# Author     : Larry Ruckman <ruckman@slac.stanford.edu>
# Created    : 2016-11-17
# Last update: 2016-11-17
#-----------------------------------------------------------------------------
# Description:
# PyRogue _chargeInj Module
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

class asicRxIDelay(pr.Device):
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs) 
                        

        for i in range(14):
            self.add(pr.RemoteVariable(name='iDelay%01i'%(i), offset=(4*i), bitSize=5, bitOffset=0, base=pr.UInt, disp = '{:#x}', mode='RW')) 
       
        self.add(pr.RemoteVariable(name='Phase', offset=14*4, bitSize=14, bitOffset=0, base=pr.UInt, disp = '{:#x}', mode='RW'))
        self.add(pr.RemoteVariable(name='iDelayAll', offset=(4*15), bitSize=5, bitOffset=0, base=pr.UInt, disp = '{:#x}', mode='WO')) 

                
