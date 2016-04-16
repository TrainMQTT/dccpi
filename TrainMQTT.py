class TrainMQTT:
	fromHere = {}

	def deserialize(self, nvp):
		base = {}
		list = nvp.split('&')
		for pair in list:
			nv = pair.split('=')
			if len(nv) == 2:
				value = u""
				value = unicode(nv[1],'utf-8')
				if value.isnumeric():
					value = int(value)
				elif value.isdecimal():
					value = float(value)
				base[nv[0]] = value
		return base

	def mapFrom(self, obj):
		self.fromHere = obj
		return self

	def mapTo(self, obj):
		for propertyName in dir(obj):
			if hasattr(obj, propertyName) and propertyName in self.fromHere:
				setattr(obj, propertyName, self.fromHere[propertyName])
		return self
