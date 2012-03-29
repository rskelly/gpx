import os
from xml.parsers.expat import *

class Gpx:

	def __init__(self):
		self.metadata = {}
		self.tracks = []
		self.routes = []
		
	def save(self, filename):
		pass
		
	@staticmethod
	def load(filename):
		parser = ParserCreate()
		handler = GpxSaxHandler()
		parser.StartElementHandler = handler.__startElement;
		parser.EndElementHandler = handler.__endElement;
		parser.ParseFile(filename)
		return parser.gpx
			
	@staticmethod
	def _parseTime(time):
		return None
		