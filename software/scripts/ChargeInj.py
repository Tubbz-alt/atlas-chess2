
class ChargeInj():
	def __init__(self,matrix=1,pulse_width=4700,pulse_delay=0,inv_pulse=False,inh_pulse=1):
		self.matrix = matrix
		self.pulse_width = pulse_width
		self.pulse_delay = pulse_delay
		self.inv_pulse = inv_pulse #invert
		self.inh_pulse = inh_pulse #inhibit
		
	def init(self,chess_control):
		chess_control.set_pulse_width(self.pulse_width)
		chess_control.set_pulse_delay(self.pulse_delay)
		chess_control.set_inv_pulse(self.inv_pulse)
		chess_control.set_inh_pulse(self.inh_pulse)
	def get_valid_hits(self,chess_control):
		return chess_control.get_valid_hits(self.matrix)
	def get_det_rows(self,chess_control):
		return chess_control.get_det_rows(self.matrix)
	def get_det_cols(self,chess_control):
		return chess_control.get_det_cols(self.matrix)
	def get_det_times(self,chess_control):
		return chess_control.get_det_times(self.matrix)
	def get_data_from_pulse(self,chess_control):
		return chess_control.get_8hits_data(self.matrix)

