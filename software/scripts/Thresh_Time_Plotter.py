import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation
from matplotlib.lines import Line2D
import numpy as np
import sys
import time

class Thresh_Time_Plotter:
	def __init__(self,shape,fig_title):
		#shape is (rows,cols) 
		#x_list = [int(x*3300/4096) for x in x_list] #convert from channel to milivolts
		self.max_time = 10000 #absolute limit
		self.x = []#[0 for i in range(0,self.max_time,self.bin_width)]
		self.y = []
		self.fig_title = fig_title
		#self.data = np.zeros(shape)
		plt.ion()
		self.fig, self.ax = plt.subplots(1,1)
		self.fig.suptitle(self.fig_title, fontsize=10)

		self.max_x = 100
		self.max_y = 100
		#we want lines to have data from columns, so reshape data
		#self.lines = self.ax.plot(np.transpose(self.data))
		#self.ax.axvline(x=vline_x*3300/4096,ymin=0,ymax=1,color='r')
		self.ax.set_autoscale_on(True)
		point_size = 2
		self.sc = self.ax.scatter(self.x,self.y,s=point_size)
		#self.ax.set_xlim(x_list[0],x_list[-1])
		self.x_label = "Time (ns)"
		self.ax.set_xlabel(self.x_label)
		self.ax.set_ylabel("Threshold Voltage (mV)")
		self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

	def relim(self):
		self.ax.set_xlim(0,self.max_x)
		self.ax.set_ylim(min(self.y),self.max_y)
		#plt.xlim(0,self.max_x)
		#plt.ylim(0,self.max_y)

	def add_data(self,t,thresh_chan):
		conv = lambda ch: int(ch*3300/4096)
		thresh = conv(thresh_chan)
		self.x.append(t)
		self.y.append(thresh)
		

		if t > self.max_x and t < self.max_time: 
			self.max_x = t
		if thresh > self.max_y:
			self.max_y = thresh

	def show(self):
		plt.pause(0.2)

	def close(self):
		plt.close(self.fig)
	
	def plot(self):
		self.fig.canvas.restore_region(self.background)
		self.relim()
		#get rid of zeros
		#plot_x,plot_y = self.rem_zeros()
		#print(self.y)
		self.sc.set_offsets(np.c_[self.x,self.y])
		#print(n)
		#print(n.tolist())
		#self.x = new_x.tolist() #from np.ndarray
		#print(self.x)
		#print(self.x,self.y)
		plt.show()
		self.ax.relim()
		self.ax.autoscale_view(True,True,True)
		self.fig.canvas.blit(self.ax.bbox)

