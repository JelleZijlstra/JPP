'''Run tests for components of the program'''

import serial_util

# files to run tests from
import charmatrix
import exhaustive
import fuser
import list_tree
import tree
import tree_parse

TESTABLE = [charmatrix, exhaustive, fuser, list_tree, tree, tree_parse]

def run():
	print 'Running tests...'
	for module in TESTABLE:
		serial_util.time_serial(module.run_tests, label=module.__name__)
