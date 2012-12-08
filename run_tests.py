'''Run tests for components of the program'''

import serial_util

# files to run tests from
import charmatrix
import exhaustive
import fuser

TESTABLE = [charmatrix, exhaustive, fuser]

def run():
	print 'Running tests...'
	for module in TESTABLE:
		serial_util.time_serial(module.run_tests, label=module.__name__)
