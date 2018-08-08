
class ChargeInj():
	def __init__(self,matrix=1):
		self.matrix = matrix
		self.pulse_width = -1
	def set_pulse_width(self,chess_control,system,pulse_width=100):
		self.pulse_width = pulse_width
		chess_control.set_pulse_width(system,pulse_width)
	def send_pulse(self,chess_control,system):
		chess_control.send_pulse(system)
	def get_valid_hits(self,chess_control,system):
		return chess_control.get_valid_hits(system,self.matrix)
	def get_det_rows(self,chess_control,system):
		return chess_control.get_det_rows(system,self.matrix)
	def get_det_cols(self,chess_control,system):
		return chess_control.get_det_cols(system,self.matrix)
	def get_det_times(self,chess_control,system):
		return chess_control.get_det_times(system,self.matrix)
	def get_data_from_pulse(self,chess_control,system):
		#only return valid data
		data = []
		det_rows = self.get_det_rows(chess_control,system)
		det_cols = self.get_det_cols(chess_control,system)
		det_times = self.get_det_times(chess_control,system)
		det_valid_hits = self.get_valid_hits(chess_control,system)
		for hit_ind in range(len(det_rows)):
			if det_valid_hits[hit_ind]:
				data.append([self.matrix,det_rows[hit_ind],det_cols[hit_ind],det_times[hit_ind]])
		return data

