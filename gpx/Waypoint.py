class Waypoint():

	def __init__(self, lat = 0.0, lon = 0.0, ele = 0.0, time = 0):
		self.lat = lat
		self.lon = lon
		self.ele = ele
		self.time = time
		
	def __str__(self):
		print '[Waypoint: %d, %d, %d, %u]' % (self.lat, self.lon, self.ele, self.time)