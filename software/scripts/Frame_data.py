import numpy as np
import sys
np.set_printoptions(threshold=np.inf)

nrows = 128
ncols = 32

class Frame_data():
	def __init__(self,frame=None):
		self.frame = frame

		self.dvflag_M0=[]
		self.mhflag_M0=[]
		self.col_M0=[]
		self.row_M0=[]

		self.dvflag_M1=[]
		self.mhflag_M1=[]
		self.col_M1=[]
		self.row_M1=[]

		self.dvflag_M2=[]
		self.mhflag_M2=[]
		self.col_M2=[]
		self.row_M2=[]
		
		self.hitmap_t0 = np.zeros((nrows,ncols))
		self.hitmap_t1 = np.zeros((nrows,ncols))
		self.hitmap_t2 = np.zeros((nrows,ncols))

	def __str__(self):
		msg = str("Hitmap 0 (self.hitmap_t0):"+str(self.hitmap_t0)+"\n")
		msg += str("Hitmap 1 (self.hitmap_t1):"+str(self.hitmap_t1)+"\n")
		msg += str("Hitmap 2 (self.hitmap_t2):"+str(self.hitmap_t2)+"\n")
		return msg

	@classmethod
	def decode_data_16b(cls,dat):
		row = dat[0] & 0x7F
		col = ((dat[1] & 0x0F) << 1) | (dat[0] >> 7)
		multi_hit  = (dat[1] & 0x10) >> 4
		data_valid = (dat[1] & 0x20) >> 5
		#dec_ok     = (dat[1] & 0xC0) >> 6
		return data_valid, multi_hit, col, row

	def decode_data(self,dat):
		if not all(d == 0 for d in dat): #To speed things up - most frames have empty data
			for i in range(0,len(dat),8):
				[li.append(el) for el,li in zip(list(self.decode_data_16b(dat[i+0:i+2])),[self.dvflag_M0, self.mhflag_M0, self.col_M0, self.row_M0])]
				[li.append(el) for el,li in zip(list(self.decode_data_16b(dat[i+2:i+4])),[self.dvflag_M1, self.mhflag_M1, self.col_M1, self.row_M1])]
				[li.append(el) for el,li in zip(list(self.decode_data_16b(dat[i+4:i+6])),[self.dvflag_M2, self.mhflag_M2, self.col_M2, self.row_M2])]

				self.hitmap_t0[self.row_M0[-1]][self.col_M0[-1]] += self.dvflag_M0[-1]
				self.hitmap_t1[self.row_M1[-1]][self.col_M1[-1]] += self.dvflag_M1[-1]
				self.hitmap_t2[self.row_M2[-1]][self.col_M2[-1]] += self.dvflag_M2[-1]

	def print_header(self):
		print("BEGIN HEADER")
		#print("virt_chan_id =",self.virt_chan_id)
		#print("dest_id =",self.dest_id)
		#print("transact_id =",self.transact_id)
		#print("acq_cnt =",self.acq_cnt)
		#print("op code =",self.op_code)
		#print("elem_id =",self.elem_id)
		#print("dest_z_id =",self.dest_z_id)
		#print("frame_nb =",self.frame_nb)
		#print("ticks =",self.ticks)
		#print("fiducials =",self.fiducials)
		#print("sbtemp =",self.sbtemp)
		#print("frame_typ =",self.frame_typ)
		print("timestamp =",self.timestamp)
		print("ticks part1 =",self.ticks_part1)
		print("ticks part2 =",self.ticks_part2<<16)
		print("fiducials part1 =",self.fiducials_part1<<32)
		print("fiducials part2 =",self.fiducials_part2<<48)
		print("frame size =",self.frame_size)
		print("END HEADER")
	def decode_header(self, header):
		#print("HEADER:",header)
		#self.virt_chan_id = header[0] & 0x01
		#self.dest_id      = header[0] & 0xFC
		#self.transact_id  = (header[3] <<16) & (header[2] << 8) & header[1]
		#self.acq_cnt      = (header[5] << 8) & header[4]
		#self.op_code      = header[6]
		#self.elem_id      = header[7] & 0x0F
		#self.dest_z_id    = header[7] >> 4
		#self.frame_nb     = (header[11] << 8*3) & (header[10] << 8*2) & (header[9] << 8) & header[8]
		#self.ticks        = (header[15] << 8*3) & (header[14] << 8*2) & (header[13] << 8) & header[12]
		#self.fiducials    = (header[19] << 8*3) & (header[18] << 8*2) & (header[17] << 8) & header[16]
		#self.sbtemp       = [	(header[27] <<8  & header[26]),
		#			(header[25] <<8  & header[24]),
		#			(header[23] <<8  & header[22]),
		#			(header[21] <<8  & header[20])]
		#self.frame_typ    = (header[31] << 8*3) & (header[30] << 8*2) & (header[29] << 8) & header[28]
		self.ticks_part1 = header[6] & 0xffff 	
		self.ticks_part2 = header[7] & 0xffff
		self.fiducials_part1 = header[8] & 0xffff
		self.fiducials_part2 = header[9] & 0xffff
		self.timestamp = np.uint64()
		self.frame_size = np.uint32()
		self.timestamp += self.ticks_part1 + (self.ticks_part2 << 16) + \
							(self.fiducials_part1 << 32) + (self.fiducials_part2 << 48)
		self.frame_size += (header[16] << 16) + header[17]
		
	def decode_frame(self):
		header, data = self.frame[:32],self.frame[32:]
		self.decode_data(data)
		self.decode_header(header)
	def get_data(self):
		#return chunk of data about most recent frame
		datalines = []
		for m in range(3):
			this_hitmap = eval("self.hitmap_t"+str(m))
			for r in range(nrows):
				for c in range(ncols):	
					nhits = int(this_hitmap[r][c])
					if nhits > 0:
						datalines.append([m,r,c,nhits])
		return datalines	
	def print_valid_data(self):
		#We check if we have non-empty lists
		if self.dvflag_M0 or self.dvflag_M1 or self.dvflag_M2:
			print("Matrix 0 - Row: {0}, Col: {1}".format(self.row_M0,self.col_M0))
			print("Matrix 1 - Row: {0}, Col: {1}".format(self.row_M1,self.col_M1))
			print("Matrix 2 - Row: {0}, Col: {1}".format(self.row_M2,self.col_M2))
