import sys
#makes system.feb.Chess2Ctrl commands easier to use
class ChessControl(): 
  nrows,ncols = 128,32
  def __init__(self,system):
    self.system = system
  def start(self):
    self.system.start(pollEn=True, pyroGroup=None, pyroHost=None)
  def stop(self):
    self.system.stop()
  def read_config(self,config_file):
    self.system.root.ReadConfig(config_file)
  def set_pktWordSize(self,size=255):
    self.system.feb.sysReg.pktWordSize.set(size)
  def software_trig(self):
    self.system.feb.sysReg.softTrig()
  def open_stream(self):
    self.system.feb.sysReg.timingMode.set(0)
  def close_stream(self):
    self.system.feb.sysReg.timingMode.set(3)
  def set_run_rate(self,rate):
    self.system.runControl.runRate.set(int(rate))
  def set_run_state(self,b):
    self.system.runControl.runState.set(b) #1 on, 0 off
  def set_threshold(self,threshold):
    self.system.feb.dac.dacPIXTHRaw.set(threshold)
  def set_baseline(self,baseline):
    self.system.feb.dac.dacBLRaw.set(baseline)
  def set_baseline_res(self,baseline_res):
    self.system.feb.dac.dacBLRRaw.set(baseline_res)
  def get_det_rows(self,matrix):
    det_rows = []
    for ind in range(8):
      det_rows.append(eval("int(self.system.feb.chargeInj.hitDetRow"+str(matrix)+"_"+str(ind)+".get())"))
    return det_rows #0 <= len() <= 8
  def get_det_cols(self,matrix):
    det_cols = []
    for ind in range(8):
      det_cols.append(eval("int(self.system.feb.chargeInj.hitDetCol"+str(matrix)+"_"+str(ind)+".get())"))
    return det_cols
  def get_det_times(self,matrix):
    det_times = []
    for ind in range(8):
      det_times.append(eval("float(self.system.feb.chargeInj.hitDetTime"+str(matrix)+"_"+str(ind)+".get())"))
    return det_times
  def get_valid_hits(self,matrix):
    det_valid_hits = []
    for ind in range(8):
      det_valid_hits.append(eval("self.system.feb.chargeInj.hitDetValid"+str(matrix)+"_"+str(ind)+".get()"))
    return det_valid_hits
  def get_8hits_data(self,matrix):
    #only return valid data, len(data) <= 8
    data = []
    det_rows = self.get_det_rows(matrix)
    det_cols = self.get_det_cols(matrix)
    det_times = self.get_det_times(matrix)
    det_valid_hits = self.get_valid_hits(matrix)
    for hit_ind in range(len(det_rows)):
        if det_valid_hits[hit_ind]:
            row,col,time = det_rows[hit_ind],det_cols[hit_ind],det_times[hit_ind]
            #if hit_ind > 0:
            #    #ignore repeated hits of same pixel
            #    if row == data[-1][1] and col == data[-1][2]:
            #        continue
            data.append([matrix,row,col,time])
    return data
  def set_pulse_width(self,pw):
    #arg in units of 3.125ns (1/320MHz)
    self.system.feb.chargeInj.pulseWidthRaw.set(pw)
  def set_pulse_delay(self,pd):
    self.system.feb.chargeInj.pulseDelayRaw.set(pd)
  def set_inv_pulse(self,b): #b is bool
    self.system.feb.chargeInj.invPulse.set(b) 
  def set_inh_pulse(self,b): 
    self.system.feb.chargeInj.calPulseInh.set(b)
  def send_pulse(self):
    self.system.feb.chargeInj.calPulse.set(1)
  def toggle_pixel(self,row,col,enable=1,which_matrix=0,all_matrices=True):
    chargeInj = 0 if enable else 1

    if all_matrices:
        for i in range(0,3):
            eval("self.system.feb.Chess2Ctrl"+str(i)+".writePixel(enable="+str(enable)+",chargeInj="+str(chargeInj)+",col=col,row=row)")
    else:
        eval("self.system.feb.Chess2Ctrl"+str(which_matrix)+".writePixel(enable="+str(enable)+",chargeInj="+str(chargeInj)+",col=col,row=row)")

  def toggle_block(self,topleft,shape=(8,1),enable=1,which_matrix=0,all_matrices=True):
    for r in range(shape[0]):
      for c in range(shape[1]):
        self.toggle_pixel(topleft[0]+r,topleft[1]+c,enable=enable,which_matrix=which_matrix,all_matrices=all_matrices)

  def enable_block(self,topleft,shape=(8,1),which_matrix=0,all_matrices=True):
    self.toggle_block(topleft,shape=shape,enable=1,which_matrix=which_matrix,all_matrices=all_matrices)
  def disable_block(self,topleft,shape=(8,1),which_matrix=0,all_matrices=True):
    self.toggle_block(topleft,shape=shape,enable=0,which_matrix=which_matrix,all_matrices=all_matrices)
  def disable_all_pixels(self,which_matrix=0,all_matrices=True):
    if all_matrices:
        for i in range(0,3):
            eval("self.system.feb.Chess2Ctrl"+str(i)+".writeAllPixels(enable=0,chargeInj=0)")
    else:
        eval("self.system.feb.Chess2Ctrl"+str(which_matrix)+".writeAllPixels(enable=0,chargeInj=0)")
  
  def enable_all_pixels(self,which_matrix=0,all_matrices=True):
    if all_matrices:
        for i in range(0,3):
            eval("self.system.feb.Chess2Ctrl"+str(i)+".writeAllPixels(enable=1,chargeInj=1)")
    else:
        eval("self.system.feb.Chess2Ctrl"+str(which_matrix)+".writeAllPixels(enable=1,chargeInj=1)")

  def get_val(self,scan_field):
    return eval("self.system.feb."+scan_field+".get()")
  def set_val(self,scan_field,val):
    return eval("self.system.feb."+scan_field+".set("+str(val)+")")



