import numpy as np
from datetime import datetime
import os
import time
import matplotlib.animation
from ChargeInj import ChargeInj
from Thresh_Hist_Plotter import Thresh_Hist_Plotter
from Time_Hist_Plotter import Time_Hist_Plotter
from Thresh_Time_Plotter import Thresh_Time_Plotter

NOW = datetime.now().strftime("%Y-%m-%d_%H-%M")

class ScanTest():
	def __init__(self,matrix=0,scan_field=None,scan_range=range(0,32),shape=(8,1),topleft=(0,0),sleeptime=10,pulserStatus="ON",delta_BL_to_BLR=0x2d0,chargeInjEnabled=0,nPulses=50):
		self.matrix = matrix
		self.scan_field = scan_field
		self.scan_range = scan_range
		self.shape = shape
		self.topleft = topleft
		self.sleeptime = sleeptime #ms, how long to take data
		self.pulserStatus = pulserStatus
		self.delta_BL_to_BLR = delta_BL_to_BLR
		self.chargeInjEnabled = chargeInjEnabled #1 is enabled
		self.chargeInj = None #initialized soon
		self.nPulses = nPulses

		#below attr's are set later
		self.fixed_baseline = None
		self.scan_type = None #"threshold_scan" or "baseline_scan"
		self.is_th_scan = False
		self.is_bl_scan = False
		self.is_other_scan = False
		self.is_time_hist = False #puts time on x axis
		self.is_thresh_time_plot = False #thresh vs time
		self.x_vals = [] #list of x values
		self.nbins = -1 #setter func used when making time plot
		self.x_label = None #xaxis label
		self.header = None #used in naming files
		self.fig_title = None #title of figure
		self.vline_x = -1 #x value of vertical line
		self.trial = 1 #used when doing repeated tests
		self.scan_dir = "../../Chess2Data/"+NOW
		self.init_savedirs()

	def init_savedirs(self):
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
	def set_sleeptime(self,sleeptime):
		self.sleeptime = sleeptime
	def set_pulserStatus(self,pulserStatus):
		self.pulserStatus = pulserStatus
	def set_chargeInjEnabled(self,b):
		self.chargeInjEnabled = b 
	def set_nPulses(self,n):
		self.nPulses = n
	def enable_block(self,chess_control):
		chess_control.enable_block(topleft=self.topleft,shape=self.shape,which_matrix=self.matrix,all_matrices=False)
	def disable_block(self,chess_control):
		chess_control.disable_block(topleft=self.topleft,shape=self.shape,which_matrix=self.matrix,all_matrices=False)
	def set_scan_type(self,scan_type):
		#scan_type is "threshold_scan" or "baseline_scan"
		if scan_type == "threshold_scan": #x axis will be baselines
			self.is_th_scan = True
		elif scan_type == "baseline_scan": #x axis will be thresholds
			self.is_bl_scan = True
		else: #x axis will be thresholds
			self.is_other_scan = True
	def set_time_hist(self,is_time_hist=False):
		self.is_time_hist = is_time_hist
	def set_thresh_time_plot(self,is_thresh_time_plot=False):
		self.is_thresh_time_plot = is_thresh_time_plot
		
	def set_x_vals(self,x_vals):
		self.x_vals = x_vals
	def set_nbins(self,nbins):
		self.nbins = nbins
	def save_fig(self,hist_fig):
		#save figure to Desktop
		fig_filename = self.header+"_trial_1.png"
		fig_path = self.fig_savedir+"/"+fig_filename
		if os.path.isfile(fig_path): 
			self.trial += 1
			fig_path = fig_path[:-5-int(self.trial/10)]+str(self.trial)+".png"
		hist_fig.fig.savefig(fig_path)
		print("Just saved fig")
	def save_fig_config(self,field_vals_msg):
		fig_config_filename = self.header+"_config.txt"
		with open(self.config_file_dir+"/"+fig_config_filename,"w") as f:
			f.write(field_vals_msg)

	def get_config_msg(self,x,val,runrate,param_config_info,start_time,stop_time):
		msg = "Start: "+start_time.strftime("%c")+"\t Stop: "+stop_time.strftime("%c")+"\n"
		deltatime = stop_time-start_time
		msg += "Topleft: "+str(self.topleft)+"\n"
		msg += "Shape: "+str(self.shape)+"\n"
		msg += "Delta: "+str(deltatime.seconds)+" seconds\n"
		msg += "Runrate: "+str(runrate)+"Hz\n"
		msg += "Sleeptime: "+str(self.sleeptime)+"ms between trigs\n"
		msg += "Pulser status: "+self.pulserStatus+"\n"
		msg += "Charge injection: "+["disabled","enabled"][self.chargeInjEnabled]+"\n"
		conv = lambda ch: int(ch*3300/4096)
		if self.is_th_scan:
			msg += "Threshold: "+str(conv(val))+"mV\n"
			msg += "Scanned thru baseline range:"+str(conv(self.x_vals[0]))+" to "+str(conv(x))+" mV\n"
		elif self.is_bl_scan: 
			msg += "Baseline: "+str(conv(val))+"mV\n"
			msg += "Scanned threshold range:"+str(conv(self.x_vals[0]))+" to "+str(conv(x))+" mV\n"
		else: #parameter scan. write baseline because xaxis is thresholds for now
			msg += "Baseline: "+str(conv(self.fixed_baseline))+"mV\n"
			msg += "Scanned threshold range:"+str(conv(self.x_vals[0]))+" to "+str(conv(x))+" mV\n"

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
			if self.is_th_scan:
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

	def init_scan(self,val,runrate):
		self.header = "runrate="+str(runrate)+",sleeptime="+str(self.sleeptime)+"ms,pulser="+self.pulserStatus+","+self.scan_field+"="+str(val)+",chargeInjEnabled="+str(self.chargeInjEnabled)
		self.fig_title = "topleft="+str(self.topleft)+",shape="+str(self.shape)+","+self.scan_field+"="+hex(val)+",chargeInjEnabled="+str(self.chargeInjEnabled)+",trial="+str(self.trial)
		if self.is_bl_scan: 
			self.x_label = "Threshold Voltage (mV)"
		elif self.is_th_scan:
			self.x_label = "Baseline Voltage (mV)"
		else: #scanning Chess2Ctrl param, x axis is thresholds for now
			self.x_label = "Threshold Voltage (mV)"
			self.header += ",dac.dacBLRaw="+str(self.fixed_baseline)


		if len(self.x_vals) == 0: 
			raise("length of x_vals is zero")
		
		if self.is_bl_scan or self.is_th_scan:
			self.vline_x = val
		else: 
			if self.fixed_baseline == None:
				raise("Fixed_baseline not set for "+self.scan_field)
			self.vline_x = self.fixed_baseline
		
	def set_x_val(self,chess_control,x):
		if self.is_th_scan:
			chess_control.set_baseline(x)
			chess_control.set_baseline_res(x+self.delta_BL_to_BLR)
		else: #bl_scan or other, either way xaxis is thresholds
			chess_control.set_threshold(x)
	
	def add_data_to_thresh_hist_fig(self,figs,eventReader):
		for fig in figs:
			if fig.__class__.__name__ == "Thresh_Hist_Plotter":
				eval("fig.add_data(eventReader.plotter.data"+str(self.matrix)+"[self.topleft[0]:self.topleft[0]+self.shape[0],self.topleft[1]:self.topleft[1]+self.shape[1]])")

	def add_data_to_time_hist_fig(self,time_hist_fig,dat):
		#should be made to inform time_fig of m,r,c...but not necessary now
		for hit in dat:
			m,r,c,t = hit
			time_hist_fig.add_hit(t)
	
	def add_data_to_thresh_time_fig(self,thresh_time_fig,dat,x):
		for hit in dat:
			m,r,c,t = hit
			thresh_time_fig.add_data(t,x)
				
	def add_data_to_time_figs(self,figs,dat,x):
		for fig in figs:
			which_fig = fig.__class__.__name__
			if which_fig == "Time_Hist_Plotter" and self.chargeInjEnabled and self.is_time_hist:
				#make hits vs time
				self.add_data_to_time_hist_fig(fig,dat)
			elif which_fig == "Thresh_Time_Plotter" and self.chargeInjEnabled and self.is_thresh_time_plot:
				#add data to thresh vs time fig
				self.add_data_to_thresh_time_fig(fig,dat,x)
			else:
				pass #ignore Thresh_hist_fig

	def init_chargeInj(self,chess_control,pulse_width=15000,pulse_delay=0,inv_pulse=False,inh_pulse=False):
		dt_nano = pulse_width #ns
		ncycles = int(dt_nano / 3.125)
		self.chargeInj = ChargeInj(matrix=self.matrix,
									pulse_width=ncycles,
									pulse_delay=pulse_delay,
									inv_pulse=inv_pulse,
									inh_pulse=inh_pulse)
		self.chargeInj.init(chess_control)

	def scan(self,chess_control,eventReader,param_config_info,runrate):
		if self.scan_field == None:
			raise("FIELD NOT SET FOR SCAN TEST")
		if self.is_other_scan: 
			#if scanning Chess2Ctrl param, set fixed baseline
			chess_control.set_baseline(self.fixed_baseline)
			chess_control.set_baseline_res(self.fixed_baseline+self.delta_BL_to_BLR)

		for val in self.scan_range:
			start_time = datetime.now()
			chess_control.set_val(self.scan_field,val)
			self.init_scan(val,runrate)
			figs = []
			if self.is_time_hist:
				figs.append(Time_Hist_Plotter(self.shape,self.fig_title,self.nbins))
			if self.is_thresh_time_plot:
				figs.append(Thresh_Time_Plotter(self.shape,self.fig_title))
			
			figs.append(Thresh_Hist_Plotter(self.shape,self.x_vals,self.x_label,self.fig_title,self.vline_x))

			for fig in figs: 
				fig.show()
			#x is threshold or baseline
			hist_data = [] #accumulate data in this list, then save to csv file
			hit_control_c = False
			try:
				for x in self.x_vals:
					self.set_x_val(chess_control,x)
					time.sleep(1) #wait 1sec to settle
					eventReader.hitmap_reset()
					#########################
					for pulse_ind in range(self.nPulses):
						chess_control.open_stream()
						#time.sleep(2.0)
						print("taking data")
						
						#chess_control.set_run_state(1)
						if self.chargeInjEnabled: 
							chess_control.send_pulse()
						#time.sleep(self.sleeptime/1000.0)
						#chess_control.set_run_state(0)
						chess_control.software_trig()
						if self.chargeInjEnabled:
							dat = self.chargeInj.get_data_from_pulse(chess_control)
							#dat is at most 8 hits (len() <= 8) [[matrix,row,col,timestamp],[..],...]

							print("Pulse data:",dat)
							#add chargeInj pulses to hitmap ?? this seems redundant
							#for hit_dat in dat:
							#	matrix,row,col = hit_dat[:3]
							#	exec("eventReader.ev_hitmap_t"+str(matrix)+"[row,col] += 1")
							#add all 8 hits to plot: x: (t1,t2,t3...), y:(nhits_t1,..)
							#sum up all hits with same time
						
						chess_control.close_stream()
						self.add_data_to_time_figs(figs,dat,x)
					
					self.add_data_to_thresh_hist_fig(figs,eventReader)

					#plot after all pulses			
					eventReader.hitmap_plot()
					for fig in figs:
						fig.plot()
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

	
			except KeyboardInterrupt:
				#save what you have, then break out of scan
				hit_control_c = True 
				self.new_scan_dir = self.scan_dir+"_PARTIAL_TEST"
				os.rename(self.scan_dir,self.new_scan_dir)
				self.scan_dir = self.new_scan_dir
				self.init_savedirs()

			#save plots,configs,and csvs
			stop_time = datetime.now()
			config_msg = self.get_config_msg(x,val,runrate,param_config_info,start_time,stop_time)
			self.save_fig_config(config_msg)
			for fig in figs:
				self.save_fig(fig)
				fig.close()
				del fig
			#save csv files with data from hist_data
			self.save_data_to_csv(hist_data)

			if hit_control_c:
				break
			
