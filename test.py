from gpx import *

g = Gpx

for file in ['examples/fells_loop.gpx', 'examples/ashland.gpx']:
	f = g.load(file)

	print "File: %s" % file
	
	print "\n	Tracks: %s" % len(f.tracks)
	for i in range(0,  len(f.tracks)):
		print "		Track %s:" % (i+1)
		for j in range(0, len(f.tracks[i].segments)):
			print "			Segment %s (%s)" % ((j+1), len(f.tracks[i].segments[j].points))

	print "\n	Waypoints %s" % len(f.waypoints)
	
	print "\n	Routes %s" % len(f.routes)
	for i in range(0, len(f.routes)):
		print "		Route %s (%s)" % ((i+1), len(f.routes[i].points))

	print "\n------------------------------------------------\n"