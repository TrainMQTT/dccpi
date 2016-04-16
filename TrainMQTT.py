class TrainMQTT:
	fromHere = {}

	def deserialize(self, nvp):
		base = {}
		print nvp
		list = nvp.split('&')
		print list
		for pair in list:
			print pair
			nv = pair.split('=')
			print nv
			base[nv[0]] = nv[1]
		return base

	def mapFrom(self, obj):
		self.fromHere = obj

	def mapTo(self, obj):
		for propertyName in dir(obj):
			if obj[propertyName] and self.fromHere[propertyName]:
				obj[propertyName] = self.fromHere[propertyName]
