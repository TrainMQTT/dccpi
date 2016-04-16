class TrainMQTT:
	def deserialize(self, nvp):
		base = {}
		list = nvp.split('&')
		for pair in list:
			nv = pair.split('=')
			base[nv[0]] = nv[1]
		return base
