import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation
from matplotlib.lines import Line2D
import numpy as np
import sys
import time

class Time_Hist_Plotter:
	def __init__(self,shape,fig_title,nbins=50):
		#shape is (rows,cols) 
		#x_list = [int(x*3300/4096) for x in x_list] #convert from channel to milivolts
		self.max_time = 10000 #absolute limit
		self.x = []#[0 for i in range(0,self.max_time,self.bin_width)]
		self.fig_title = fig_title
		#self.data = np.zeros(shape)
		plt.ion()
		self.fig, self.ax = plt.subplots(1,1)
		self.fig.suptitle(self.fig_title, fontsize=10)

		self.nbins = nbins
		self.max_x = 100
		#we want lines to have data from columns, so reshape data
		#self.lines = self.ax.plot(np.transpose(self.data))
		#self.ax.axvline(x=vline_x*3300/4096,ymin=0,ymax=1,color='r')
		self.ax.set_autoscale_on(True)
		#self.ax.set_xlim(x_list[0],x_list[-1])
		self.x_label = "Time (ns)"
		self.ax.set_xlabel(self.x_label)
		self.ax.set_ylabel("Hits")
		self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

	def relim(self):
		self.ax.set_xlim(0,self.max_x)
		#self.ax.set_ylim(0,self.max_y)
		#plt.xlim(0,self.max_x)
		#plt.ylim(0,self.max_y)

	def add_hit(self,t):
		#conform to bin, then increment y value by 1 if bin exists

		self.x.append(t)
		

		if t > self.max_x and t < self.max_time: 
			self.max_x = t

	def show(self):
		plt.pause(0.2)

	def close(self):
		plt.close(self.fig)
	
	def plot(self):
		self.fig.canvas.restore_region(self.background)
		self.relim()
		#get rid of zeros
		#plot_x,plot_y = self.rem_zeros()
		#self.sc.set_offsets(np.c_[plot_x,plot_y])
		#print(self.y)
		n,bins,ps = self.ax.hist(self.x,bins=self.nbins,range=(0,self.max_x),color='b')
		#print(n)
		#print(n.tolist())
		#self.x = new_x.tolist() #from np.ndarray
		#print(self.x)
		#print(self.x,self.y)
		plt.show()
		self.ax.relim()
		self.ax.autoscale_view(True,True,True)
		self.fig.canvas.blit(self.ax.bbox)

