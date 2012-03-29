class GpxSaxHandler:

	# Level 1
	trk = 8
	rte = 16
	met = 1
	wpt = 1024
	# Level 2
	tim = 2
	lin = 4
	seg = 32
	wpt = 64
	rpt = 2048
	ele = 128
	txt = 256
	textOn = False
	
	def __init__(self):
		self.gpx = Gpx()
		self.mode = 0
		self.currentTrack = None
		self.currentSegment = None
		self.currentRoute = None
		self.currentPoint = None
		
	def _startElement(self, name, attributes):
		if name is 'metadata':
			self.mode += met
		elif name is 'trk':
			self.mode += trk
			self.currentTrack = []
			self.gpx.tracks.append(self.currentTrack)
		elif name is 'rte':
			self.mode += rte
			self.currentRoute = []
			self.gpx.routes.append(self.currentRoute)
		elif name is 'trkseg':
			self.mode += seg
			self.currentSegment = []
			self.currentTrack.append(self.currentSegment)
		elif name is 'trkpt':
			self.mode += tpt
			self.currentPoint = Waypoint(double(attributes['lat']), double(attributes['lon']))
			self.currentTrack.append(self.currentPoint)
		elif name is 'wpt':
			self.mode += wpt
			self.currentPoint = Waypoint(double(attributes['lat']), double(attributes['lon']))
			self.gpx.waypoints.append(self.currentPoint)
		elif name is 'rtept':
			self.mode += rpt
			self.currentPoint = Waypoint(double(attributes['lat']), double(attributes['lon']))
			self.currentRoute.append(self.currentPoint)			
		elif name is 'time':
			self.mode += tim
		elif name is 'link':
			self.mode += lin
		elif name is 'text':
			self.mode += txt
		elif name is 'ele':
			self.mode += ele
		
	def _endElement(self, name):
		if name is 'metadata':
			self.mode -= met
		elif name is 'trk':
			self.mode -= trk
			self.currentTrack = None
		elif name is 'rte':
			self.mode -= rte
			self.currentRoute = None
		elif name is 'trkseg':
			self.mode -= seg
			self.currentSegment = None
		elif name is 'trkpt':
			self.mode -= tpt
			self.currentPoint = None
		elif name is 'rtept':
			self.mode -= rpt
			self.currentPoint = None
		elif name is 'wpt':
			self.mode -= wpt
			self.currentPoint = None
		elif name is 'time':
			self.mode -= tim
		elif name is 'link':
			self.mode -= lin
			self.gpx.metadata['link'] = {href:attributes['href']}
		elif name is 'text':
			self.mode -= txt
		elif name is 'ele':
			self.mode -= ele

	def _charData(self, data):
		if textOn is True:
			m = self.mode
			if (m & met) != 0:
				if (m & tim) != 0:
					self.gpx.metadata['time'] = Gpx._parseTime(data)
				elif (m & lin) != 0:
					self.gpx.metadata['link']['text'] = data
			if (m & wpt) != 0 or (m & rpt) != 0 or (m & tpt) !=0:
				if (m & tim) !=0:
					self.currentPoint.time = Gpx._parseTime(data)
				elif (m & ele) != 0:
					self.currentPoint.ele = double(data)
			elif (m & seg) != 0:
				pass
			elif (m & trk) != 0:
				pass
			
	def _elementDecl(self, name, model):
		print name
		textOn = name is 'element'
