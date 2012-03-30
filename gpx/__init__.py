import os
from xml.parsers.expat import *


class Gpx(dict):
	"""Represents a parsed GPX file (http://www.topografix.com/gpx.asp)."""
	
	def __init__(self):
		"""Initialize the GPX object. Creates empty containers for metadata, bounds, tracks, routes and waypoints."""
		self.metadata = {}
		self.bounds = {}
		self.tracks = []
		self.routes = []
		self.waypoints = []
		
	def save(self, filename):
		"""Save the GPX object to the given file."""
		# Not implemented yet. This class has no ability to handle extensions to GPX yet, so consider that when implementing.
		pass
		
	@staticmethod
	def load(filename):
		"""Loads the GPX file from the given filename and returns a Gpx object."""
		parser = ParserCreate()
		handler = GpxSaxHandler()
		parser.StartElementHandler = handler._startElement
		parser.EndElementHandler = handler._endElement
		parser.CharacterDataHandler = handler._charData
		with open(filename, 'r') as h:
			parser.ParseFile(h)
		return handler.gpx
			
	@staticmethod
	def parseTime(time):
		"""Parses a GPX time string into an integer representing the number of miliseconds since the epoch."""
		return None
		
class Route(dict):
	"""Represents a GPX route."""
	
	def __init__(self):
		"""Initialize the Route object. Creates an empty list for route points."""
		self.points = []


class Track(dict):
	"""Represents a GPX track object."""
	
	def __init__(self):
		"""Initialize the Track object. Creates an empty list for segments."""
		self.segments = []
		
class TrackSegment(dict):
	"""Represents a GPX track segment."""
	
	def __init__(self):
		"""Initializes the TrackSegment object. Creates and empty list for track points."""
		self.points = []
		
class Waypoint(dict):
	"""Represents a GPX waypoint; used for waypoints, route points and track points."""
	
	def __init__(self, lat = 0.0, lon = 0.0, ele = 0.0, time = 0):
		"""Initialize the Waypoint object."""
		self.lat = lat
		self.lon = lon
		self.ele = ele
		self.time = time
		
	def __str__(self):
		"""Represent the Waypoint as a string."""
		return '[Waypoint: %d, %d, %d, %u]' % (self.lat, self.lon, self.ele, self.time)
		
class GpxSaxHandler:
	"""A SAX handler to be used with the expat parser. Provides methods for parsing GPX files."""
	
	def __init__(self):
		"""Initialize the GpxSaxHandler."""
		self.gpx = None
		self.stack = []
		self.curName = None
		self.textOn = False
		
	def _startElement(self, name, attributes):
		"""Called when an element starts."""
		self.curName = name
		if name == 'gpx':
			self.stack.append(Gpx())
		elif name == 'bounds':
			gpx = self.stack[-1]
			gpx.bounds['minlat'] = float(attributes['minlon'])
			gpx.bounds['minlon'] = float(attributes['minlon'])
			gpx.bounds['maxlat'] = float(attributes['maxlat'])
			gpx.bounds['maxlon'] = float(attributes['maxlon'])
		elif name == 'metadata':
			# Append the gpx' metadata map to the stack.
			self.stack.append(self.stack[-1].metadata)
		elif name == 'trk':
			t = Track()
			# Append the new track to the gpx track list.
			self.stack[-1].tracks.append(t)
			# Also add to the stack.
			self.stack.append(t)
		elif name == 'rte':
			r = Route()
			# Append the new route to the gpx route list.
			self.stack[-1].routes.append(r)
			# Also add to the stack.
			self.stack.append(r)
		elif name == 'trkseg':
			s = TrackSegment()
			# Add the new segment to the track (which is the previous item in the stack).
			self.stack[-1].segments.append(s)
			self.stack.append(s)
		elif name == 'trkpt':
			w = Waypoint(float(attributes['lat']), float(attributes['lon']))
			# Add the waypoint to the segment (which is the previous item in the stack).
			self.stack[-1].points.append(w)
			self.stack.append(w)
		elif name == 'wpt':
			w = Waypoint(float(attributes['lat']), float(attributes['lon']))
			# Add the waypoint to the gpx.
			self.stack[-1].waypoints.append(w)
			# Add the waypoint to the stack.
			self.stack.append(w)
		elif name == 'rtept':
			w = Waypoint(float(attributes['lat']), float(attributes['lon']))
			# Add the waypoint to the route (which is the previous item in the stack).
			self.stack[-1].points.append(w)
			self.stack.append(w)
		elif name == 'link':
			# Add a link object to the stack.
			self.stack.append({href:attributes['href']})
		elif name in ['text', 'ele', 'sym', 'name', 'desc', 'type', 'time']:
			self.textOn = True
		
	def _endElement(self, name):
		"""Called when an element ends."""
		if name == 'gpx':
			self.gpx = self.stack.pop()
		elif name in ['metadata', 'trk', 'rte', 'trkseg', 'trkpt', 'rtept', 'wpt', 'link']:
			self.stack.pop()
		elif name in ['text', 'ele', 'sym', 'name', 'desc', 'type', 'time']:
			self.textOn = False
			self.curName = None
		
	def _charData(self, data):
		"""Called when character data is encountered."""
		if self.textOn == True:
			o = self.stack[-1]
			if o is None:
				raise "o is None"
			if self.curName == 'time':
				o['time'] = Gpx.parseTime(data)
			elif self.curName == 'ele':
				o['ele'] = float(data)
			else:
				o[self.curName] = data;

