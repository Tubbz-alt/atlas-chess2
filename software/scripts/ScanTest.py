from Hist_Plotter import Hist_Plotter
import numpy as np
from datetime import datetime
import os
import time
from ChargeInj import ChargeInj

NOW = datetime.now().strftime("%Y-%m-%d_%H-%M")

class ScanTest():
	def __init__(self,matrix=0,scan_field=None,scan_range=range(0,32),shape=(8,1),topleft=(0,0),ntrigs=5,sleeptime=10,pulserStatus="ON",delta_BL_to_BLR=0x200,chargeInjEnabled=0):
		self.matrix = matrix
		self.scan_field = scan_field
		self.scan_range = scan_range
		self.shape = shape
		self.topleft = topleft
		self.ntrigs = ntrigs #default, seems good for now--explore later
		self.sleeptime = sleeptime #ms, between each readout trig in ntrigs
		self.pulserStatus = pulserStatus
		self.delta_BL_to_BLR = delta_BL_to_BLR
		self.chargeInjEnabled = chargeInjEnabled #1 is enabled

		#below attr's are set later
		self.fixed_baseline = None
		self.scan_type = None #"threshold_scan" or "baseline_scan"
		self.is_th_scan = False
		self.is_bl_scan = False
		self.is_other_scan = False
		self.x_vals = [] #list of x values
		self.x_label = None #xaxis label
		self.header = None #used in naming files
		self.fig_title = None #title of figure
		self.vline_x = -1 #x value of vertical line

		self.scan_dir = "../../Chess2Data/"+NOW
		self.data_savedir = self.scan_dir+"/data"
		self.fig_savedir = self.scan_dir+"/plots"
		self.config_file_dir = self.scan_dir+"/config"

		if not os.path.isdir(self.data_savedir): os.makedirs(self.data_savedir)
		if not os.path.isdir(self.fig_savedir): os.makedirs(self.fig_savedir)
		if not os.path.isdir(self.config_file_dir): os.makedirs(self.config_file_dir)
	def set_matrix(self,matrix):
		self.matrix = matrix
	def set_scan_field(self,scan_field):
		self.scan_field = scan_field
	def set_scan_range(self,scan_range):
		self.scan_range = scan_range
	def set_shape(self,shape):
		self.shape = shape
	def set_fixed_baseline(self,bl):
		self.fixed_baseline = bl
	def set_topleft(self,topleft):
		self.topleft = topleft
	def set_ntrigs(self,ntrigs):
		self.ntrigs = ntrigs
	def set_sleeptime(self,sleeptime):
		self.sleeptime = sleeptime
	def set_pulserStatus(self,pulserStatus):
		self.pulserStatus = pulserStatus
	def set_chargeInjEnabled(self,b):
		self.chargeInjEnabled = b 
	def enable_block(self,chess_control,system):
		chess_control.enable_block(system,topleft=self.topleft,shape=self.shape,which_matrix=self.matrix,all_matrices=False)
	def disable_block(self,chess_control,system):
		chess_control.disable_block(system,topleft=self.topleft,shape=self.shape,which_matrix=self.matrix,all_matrices=False)
	def set_scan_type(self,scan_type):
		#scan_type is "threshold_scan" or "baseline_scan"
		if scan_type == "threshold_scan": #x axis will be baselines
			self.is_th_scan = True
		elif scan_type == "baseline_scan": #x axis will be thresholds
			self.is_bl_scan = True
		else: #x axis will be thresholds
			self.is_other_scan = True
	def set_x_vals(self,x_vals):
		self.x_vals = x_vals
	def save_fig(self,hist_fig):
		#save figure to Desktop
		fig_filename = self.header+".png"
		fig_path = self.fig_savedir+"/"+fig_filename
		#add "_trial_<#>" before ".png" if all configs are the same (repeated trials)
		i = 1
		if os.path.isfile(fig_path): 
			fig_path = fig_path[:-4]+"_trial_"+str(i)+".png"
			while os.path.isfile(fig_path): 
				i += 1
				fig_path = fig_path[:-5-int(i/10)]+str(i)+".png"
			
		hist_fig.fig.savefig(fig_path)
		print("Just saved fig")
	def save_fig_config(self,field_vals_msg):
		fig_config_filename = self.header+"_config.txt"
		with open(self.config_file_dir+"/"+fig_config_filename,"w") as f:
			f.write(field_vals_msg)
		f.close()

	def get_config_msg(self,system,val,param_config_info,start_time,stop_time):
		msg = "Start: "+start_time.strftime("%c")+"\t Stop: "+stop_time.strftime("%c")+"\n"
		deltatime = stop_time-start_time
		msg += "Topleft: "+str(self.topleft)+"\n"
		msg += "Shape: "+str(self.shape)+"\n"
		msg += "Delta: "+str(deltatime.seconds)+" seconds\n"
		msg += "Ntrigs: "+str(self.ntrigs)+"\n"
		msg += "Sleeptime: "+str(self.sleeptime)+"ms between trigs\n"
		msg += "Pulser status: "+self.pulserStatus+"\n"
		msg += "Charge injection: "+["disabled","enabled"][self.chargeInjEnabled]+"\n"
		if self.is_th_scan:
			msg += "Threshold channel: "+str(val)+"\n"
		elif self.is_bl_scan: 
			msg += "Baseline channel: "+str(val)+"\n"
		else: #parameter scan. write baseline because xaxis is thresholds for now
			msg += "Baseline channel: "+str(self.fixed_baseline)+"\n"

		msg += "Scan param: "+self.scan_field+"\n"
		#now add lines specifying parameter config
		for param_line in param_config_info.split(",")[:-1]:
			if self.scan_field in param_line: 
				continue
			msg += param_line+"\n"
		return msg

	def save_data_to_csv(self,hist_data):
		csv_filename = self.header+".csv"
		f = open(self.data_savedir+"/"+csv_filename,"w")
		for xind in range(len(hist_data)):
			xval = hist_data[xind][0][0][0]
			if self.is_bl_scan:
				f.write("Baseline "+str(xval)+":\n")
			else: 
				f.write("Threshold "+str(xval)+":\n")
			for frameind in range(len(hist_data[xind])):
				f.write("\tFrame "+str(frameind)+":\n")
				for pix in hist_data[xind][frameind]:
					#write line of pix, (th,m,r,c,nhits) w/o th
					msg = "\t\t"+str(pix[1])
					for v in pix[2:]: 
						msg += ","+str(v)
					msg += "\n"
					f.write(msg)	
		f.close()

	def init_scan(self,val):
		self.header = "ntrigs="+str(self.ntrigs)+",sleeptime="+str(self.sleeptime)+"ms,pulser="+self.pulserStatus+","+self.scan_field+"="+str(val)+",chargeInjEnabled="+str(self.chargeInjEnabled)
		self.fig_title = "topleft="+str(self.topleft)+",shape="+str(self.shape)+","+self.scan_field+"="+str(val)+",chargeInjEnabled="+str(self.chargeInjEnabled)
		if self.is_bl_scan: 
			self.x_label = "Threshold Voltage Channel (~3.3V at channel 4096)"
		elif self.is_th_scan:
			self.x_label = "Baseline Voltage Channel (~3.3V at channel 4096)"
		else: #scanning Chess2Ctrl param, x axis is thresholds for now
			self.x_label = "Threshold Voltage Channel (~3.3V at channel 4096)"
			self.header += ",dac.dacBLRaw="+str(self.fixed_baseline)

		if len(self.x_vals) == 0: 
			raise("length of x_vals is zero")
		
		if self.is_bl_scan or self.is_th_scan:
			self.vline_x = val
		else: 
			if self.fixed_baseline == None:
				raise("Fixed_baseline not set for "+self.scan_field)
			self.vline_x = self.fixed_baseline
		
	def set_x_val(self,chess_control,system,x):
		if self.is_th_scan:
			#BL and BLR should be 144 from each other, according to Herve, but
				#Dionisio has 0x200 from each other as in ppt
			chess_control.set_baseline(system,x)
			chess_control.set_baseline_res(system,x+self.delta_BL_to_BLR)
		else: #bl_scan or other, either way xaxis is thresholds
			chess_control.set_threshold(system,x)

	def check_key_press(self,hist_fig):
		#CURRENTLY ONLY REGISTERS KEY PRESS DURING TIME BETWEEN PLOTTING
		#if this plot is boring (no data), allow user
		# to skip this field val by pressing 'n' key
		if hist_fig.hit_n_key:
			eventReader.reset_data_frames()
			hist_fig.hit_n_key = False
			print("SKIPPING THIS PLOT")
			return True

	def scan(self,chess_control,system,eventReader,param_config_info):
		if self.scan_field == None:
			raise("FIELD NOT SET FOR SCAN TEST")
		if self.is_other_scan: 
			#if scanning Chess2Ctrl param, set fixed baseline
			chess_control.set_baseline(system,self.fixed_baseline)
			chess_control.set_baseline_res(system,self.fixed_baseline+self.delta_BL_to_BLR)

		#init chargeInj object
		if self.chargeInjEnabled:
				#pulse_width=multiple of 3.125ns
				dt_nano = 15000 #ns, same as yubo as of 8/17/18 
				ncycles = int(dt_nano / 3.125)
				chargeInj = ChargeInj(matrix=self.matrix,
											pulse_width=ncycles,
											pulse_delay=0,
											inv_pulse=False,
											inh_pulse=1) #0=inhibit ????
				chargeInj.init(chess_control,system)

		for val in self.scan_range:
			start_time = datetime.now()
			eval("system.feb."+self.scan_field+".set("+str(val)+")")
			self.init_scan(val)
			hist_fig = Hist_Plotter(self.shape,self.x_vals,self.x_label,self.fig_title,self.vline_x)
			hist_fig.show()
			#x is threshold or baseline
			hist_data = []
			for x in self.x_vals:
				self.set_x_val(chess_control,system,x)
				eventReader.hitmap_reset()
				#########################
				system.feb.sysReg.timingMode.set(0x0) #enable data stream
				time.sleep(1.0)
				print("taking data")
				
				trig_count = 0
				pulse_data = [] #used for chargeInj pulses
				while trig_count < self.ntrigs:	
					if self.chargeInjEnabled: 
						chargeInj.send_pulse(chess_control,system)
					time.sleep(self.sleeptime/1000.0)
					system.feb.sysReg.softTrig()
					if self.chargeInjEnabled:
						dat = chargeInj.get_data_from_pulse(chess_control,system)
						#dat is at most 8 hits (len() <= 8) [[matrix,row,col,timestamp],[..],...]
						if len(dat) > 0:
							pulse_data.append(dat)
					trig_count += 1
				system.feb.sysReg.timingMode.set(0x3) #stop taking data
				#########################

				if self.chargeInjEnabled:
					print("Pulse data:",pulse_data)
					#add chargeInj pulses to hitmap ?? this seems redundant
					for hit_dat in dat:
						matrix,row,col = hit_dat[:3]
						exec("eventReader.ev_hitmap_t"+str(matrix)+"[row,col] += 1")



				eventReader.hitmap_plot()
				eval("hist_fig.add_data(eventReader.plotter.data"+str(self.matrix)+"[self.topleft[0]:self.topleft[0]+self.shape[0],self.topleft[1]:self.topleft[1]+self.shape[1]])")
				hist_fig.plot()
				#if this plot is boring (no data), allow user
				# to skip this field val by pressing 'n' key
				if self.check_key_press(hist_fig):
					break #skip this plot

				dfs = eventReader.get_data_frames()
				#dfs = [ [ [m,r,c],[m,r,c],...], ...]
				#print("Data frames:",dfs)
				
				#Before appending to hist data, insert threshold into each pix hit
				for i in range(len(dfs)):
					for j in range(len(dfs[i])):
						dfs[i][j].insert(0,x)
				#dfs = [ [ [x,m1,r1,c1],[x,m2,r2,c2],...], ...]
				if len(dfs) > 0: 
					hist_data.append(dfs)
				eventReader.reset_data_frames()
			#save plots,configs,and csvs
			stop_time = datetime.now()
			self.save_fig(hist_fig)
			config_msg = self.get_config_msg(system,val,param_config_info,start_time,stop_time)
			self.save_fig_config(config_msg)
			hist_fig.close()
			del hist_fig
			#save csv files with data from hist_data
			self.save_data_to_csv(hist_data)
