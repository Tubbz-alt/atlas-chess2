import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation
from matplotlib.lines import Line2D
import numpy as np
import sys
import time

class Time_Plotter:
	def __init__(self,shape,fig_title):
		#shape is (rows,cols) 
		#x_list = [int(x*3300/4096) for x in x_list] #convert from channel to milivolts
		self.x,self.y = [],[]
		self.time_hits = {} #time_valid["125.25"] = 0 if not in self.x
		self.fig_title = fig_title
		#self.data = np.zeros(shape)
		plt.ion()
		self.fig, self.ax = plt.subplots(1,1)
		self.fig.suptitle(self.fig_title, fontsize=10)

		self.sc = self.ax.scatter(self.x,self.y,s=10,alpha=0.75)
		self.max_x = 100
		self.max_y = 3
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
		plt.xlim(0,self.max_x)
		plt.ylim(0,self.max_y)

	def add_hit(self,t):
		try:
			self.time_hits[str(t)] += 1
			#below line is slow, could be improved
			self.y[self.x.index(t)] += 1
		except KeyError:
			self.time_hits[str(t)] = 1
			self.x.append(t)
			self.y.append(1)

		if t > self.max_x: self.max_x = t
		if self.y[-1] > self.max_y: self.max_y = self.y[-1]		

	def show(self):
		plt.pause(0.2)

	def close(self):
		plt.close(self.fig)
	
	def plot(self):
		#plt.draw()
		self.fig.canvas.restore_region(self.background)
		self.relim()
		#self.ax.autoscale_view(True,True,True)
		#0th index of x_data is unused, same with line_y (extra from init)
		#self.ax.set_data(self.x_data[1:len(line_y)], line_y[1:])
		self.sc.set_offsets(np.c_[self.x,self.y])
		#print(self.x,self.y)
		plt.show()
		self.ax.relim()
		#self.ax.autoscale_view()
		#self.ax.draw_artist(self.lines[i])
		#self.ax.relim()
		#self.ax.autoscale_view(True,True,True)
		#plt.plot((800,800), (0, maxy), 'k-')
		self.fig.canvas.blit(self.ax.bbox)

