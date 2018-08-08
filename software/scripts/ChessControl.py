import sys
#makes system.feb.Chess2Ctrl commands easier to use
class ChessControl(): 
  def __init__(self):
    self.threshold = 0
    self.nrows = 128
    self.ncols = 32
    #self.starting_coords = [(r,c) for r in range(0,self.nrows-1,8) for c in range(0,self.ncols)]
    #self.starting_coords = [(r,c) for r in range(0,64,8) for c in range(0,32)]
  def set_threshold(self,system,threshold):
    system.feb.dac.dacPIXTHRaw.set(threshold)
  def set_baseline(self,system,baseline):
    system.feb.dac.dacBLRaw.set(baseline)
  def set_baseline_res(self,system,baseline_res):
    system.feb.dac.dacBLRRaw.set(baseline_res)

##TODO: update below funcs. documentation is hitDetRow<matrix>_<index of hit[0-7]>
  def get_det_rows(self,system,matrix):
    det_rows = []
    for ind in range(8):
      det_rows.append(eval("int(system.feb.chargeInj.hitDetRow"+str(matrix)+"_"+str(ind)+".get())"))
    return det_rows #0 <= len <= 8
  def get_det_cols(self,system,matrix):
    det_cols = []
    for ind in range(8):
      det_cols.append(eval("int(system.feb.chargeInj.hitDetCol"+str(matrix)+"_"+str(ind)+".get())"))
    return det_cols
  def get_det_times(self,system,matrix):
    det_times = []
    for ind in range(8):
      det_times.append(eval("float(system.feb.chargeInj.hitDetTime"+str(matrix)+"_"+str(ind)+".get())"))
    return det_times
  def get_valid_hits(self,system,matrix):
    det_valid_hits = []
    for ind in range(8):
      det_valid_hits.append(eval("system.feb.chargeInj.hitDetValid"+str(matrix)+"_"+str(ind)+".get()"))
    return det_valid_hits



  def set_pulse_width(self,system,pw):
    #arg in units of 3.125ns (1/320MHz)
    system.feb.chargeInj.pulseWidthRaw.set(pw)
  def send_pulse(self,system):
    #pass
    system.feb.chargeInj.calPulse.set(1)
    #system.feb.chargeInj.calPulseInh.set(1) #inhibit pulse
  def set_val(self,system,scan_field,val):
    eval("system.feb."+scan_field+".set(val)")
  def toggle_pixel(self,system,row,col,enable=1,which_matrix=0,all_matrices=True):
    chargeInj = 0 if enable else 1

    if all_matrices:
        for i in range(0,3):
            eval("system.feb.Chess2Ctrl"+str(i)+".writePixel(enable="+str(enable)+",chargeInj="+str(chargeInj)+",col=col,row=row)")
    else:
        eval("system.feb.Chess2Ctrl"+str(which_matrix)+".writePixel(enable="+str(enable)+",chargeInj="+str(chargeInj)+",col=col,row=row)")

  def toggle_block(self,system,topleft,shape=(8,1),enable=1,which_matrix=0,all_matrices=True):
    for r in range(shape[0]):
      for c in range(shape[1]):
        self.toggle_pixel(system,topleft[0]+r,topleft[1]+c,enable=enable,which_matrix=which_matrix,all_matrices=all_matrices)

  def enable_block(self,system,topleft,shape=(8,1),which_matrix=0,all_matrices=True):
    self.toggle_block(system,topleft,shape=shape,enable=1,which_matrix=which_matrix,all_matrices=all_matrices)
  def disable_block(self,system,topleft,shape=(8,1),which_matrix=0,all_matrices=True):
    self.toggle_block(system,topleft,shape=shape,enable=0,which_matrix=which_matrix,all_matrices=all_matrices)
  def disable_all_pixels(self,system,which_matrix=0,all_matrices=True):
    if all_matrices:
        for i in range(0,3):
            eval("system.feb.Chess2Ctrl"+str(i)+".writeAllPixels(enable=0,chargeInj=0)")
    else:
        eval("system.feb.Chess2Ctrl"+str(which_matrix)+".writeAllPixels(enable=0,chargeInj=0)")
  
  def enable_all_pixels(self,system,which_matrix=0,all_matrices=True):
    if all_matrices:
        for i in range(0,3):
            eval("system.feb.Chess2Ctrl"+str(i)+".writeAllPixels(enable=1,chargeInj=1)")
    else:
        eval("system.feb.Chess2Ctrl"+str(which_matrix)+".writeAllPixels(enable=1,chargeInj=1)")

  def get_val(self,system,feb_field,val_field):
    return eval("system.feb."+feb_field+"."+val_field+".get()")



