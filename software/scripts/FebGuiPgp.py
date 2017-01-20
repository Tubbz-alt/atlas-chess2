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
import pyrogue.utilities.fileio
import pyrogue.gui
import AtlasChess2Feb
import threading
import signal
import atexit
import yaml
import time
import sys
import PyQt4.QtGui

# Custom run control
class MyRunControl(pyrogue.RunControl):
   def __init__(self,name):
      pyrogue.RunControl.__init__(self,name,'Run Controller')
      self._thread = None

      self.runRate.enum = {1:'1 Hz', 10:'10 Hz', 100:'100 Hz'}

   def _setRunState(self,dev,var,value):
      if self._runState != value:
         self._runState = value

         if self._runState == 'Running':
            self._thread = threading.Thread(target=self._run)
            self._thread.start()
         else:
            self._thread.join()
            self._thread = None

   def _run(self):
      self._runCount = 0
      self._last = int(time.time())

      while (self._runState == 'Running'):
         delay = 1.0 / ({value: key for key,value in self.runRate.enum.iteritems()}[self._runRate])
         time.sleep(delay)
         self._root.feb.sysReg.softTrig()

         self._runCount += 1
         if self._last != int(time.time()):
             self._last = int(time.time())
             self.runCount._updated()

# Set base
febBoard = pyrogue.Root('febBoard','Front End Board')

# Run control
febBoard.add(MyRunControl('runControl'))

# File writer
dataWriter = pyrogue.utilities.fileio.StreamWriter('dataWriter')
febBoard.add(dataWriter)

# Create the PGP interfaces
pgpVc0 = rogue.hardware.pgp.PgpCard('/dev/pgpcard_0',0,0) # Data
pgpVc1 = rogue.hardware.pgp.PgpCard('/dev/pgpcard_0',0,1) # Registers

# Display PGP card's firmware version
print("")
print("PGP Card Version: %x" % (pgpVc0.getInfo().version))
print("")

# Create and Connect SRPv0 to VC1
srp = rogue.protocols.srp.SrpV0()
pyrogue.streamConnectBiDir(pgpVc1,srp)

# Add configuration stream to file as channel 0
pyrogue.streamConnect(febBoard,dataWriter.getChannel(0x0))

# Add data stream to file as channel 1
pyrogue.streamConnect(pgpVc0,dataWriter.getChannel(0x1))

# Add registers
febBoard.add(AtlasChess2Feb.feb(memBase=srp,offset=0x0))

# Display the FEB's firmware version and build string
print("")
print("Firmware Version: 0x%08X" % (febBoard.feb.axiVersion.fpgaVersion.get()))
print("Firmware build string: %s" % (febBoard.feb.axiVersion.buildStamp.get()))
print("")

#########
# testing 
#########

# Set the default values for the ASIC cd ..

febBoard.feb.saci_0.CLK_bit_sel.set(0)
febBoard.feb.saci_0.clk_dly.set(0)
febBoard.feb.saci_0.rd_1.set(0)
febBoard.feb.saci_0.rlt_1.set(2)
febBoard.feb.saci_0.wrd_1.set(3)
febBoard.feb.saci_0.wrd_2.set(3)
febBoard.feb.saci_0.rd_2.set(0)
febBoard.feb.saci_0.rlt_2.set(2)

# febBoard.feb.saci_0.writeMatrix(enable=0,chargeInj=0,trimI=0)
# febBoard.feb.saci_1.writeMatrix(enable=0,chargeInj=0,trimI=0)
# febBoard.feb.saci_2.writeMatrix(enable=0,chargeInj=0,trimI=0)

# febBoard.feb.saci_0.writeAllRow(row=0,enable=0,chargeInj=0,trimI=0)
# febBoard.feb.saci_0.writeAllCol(col=3,enable=0,chargeInj=0,trimI=0)
# febBoard.feb.saci_0.writePixel(row=1,col=2,enable=0,chargeInj=0,trimI=0)

# febBoard.feb.saci_0.writePixel(row=0,col=0,enable=0,chargeInj=0,trimI=0)

# for row in range(128):
    # for col in range(32):
        # febBoard.feb.saci_0.writePixel(row=row,col=col,enable=0,chargeInj=0,trimI=0)
        # febBoard.feb.saci_1.writePixel(row=row,col=col,enable=0,chargeInj=0,trimI=0)
        # febBoard.feb.saci_2.writePixel(row=row,col=col,enable=0,chargeInj=0,trimI=0)
        # febBoard.feb.saci_0.writePixel(row=row,col=col,enable=0,chargeInj=0,trimI=col)

febBoard.feb.saci_0.StartMatrixConfig.post(0)       
for row in range(128):
    print ('row = %d) = 0x%x' % (row))    
    for col in range(32):
        febBoard.feb.saci_0.ColPointer.post(col)       
        febBoard.feb.saci_0.RowPointer.post(row)       
        febBoard.feb.saci_0.WritePixel.post(0)       
febBoard.feb.saci_0.EndMatrixConfig.get()     
        
# Create GUI
appTop = PyQt4.QtGui.QApplication(sys.argv)
guiTop = pyrogue.gui.GuiTop('febBoardGui')
guiTop.resize(800, 1000)
guiTop.addTree(febBoard)

# Run gui
appTop.exec_()

# Stop mesh after gui exits
febBoard.stop()
