'''Utilities for timing'''

import time

def time_serial(f, label=None, repeats=1):
	'''Takes in a function that takes no arguments; returns a tuple of the function's return value and the time it took to execute.'''
	start_time = time.time()

	# Run the function
	for i in xrange(0, repeats):
		out = f()
	end_time = time.time()
	time_taken = end_time - start_time
	if label is not None:
		print "Time for %s: %f" % (label, time_taken)
	return out, time_taken
