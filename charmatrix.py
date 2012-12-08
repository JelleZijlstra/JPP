'''
Class for representing a taxon-character matrix.

Input is in the following form:
nchars ntaxa
Taxon name	0101223

The first taxon is treated as an outgroup.
'''

import re
import numpy as np

class charmatrix(object):
	def __init__(self, filename):
		super(charmatrix, self).__init__()
		# initialize counts
		self.nchars = 0
		self.ntaxa = 0

		# open file, read nchars and ntaxa
		infile = open(filename, 'r')
		firstline = infile.readline()
		data = re.split(' ', firstline)
		self.nchars = int(data[0])
		self.ntaxa = int(data[1])

		# make array of taxon names
		self.names = np.empty(self.ntaxa, dtype=np.object_)

		# make matrix of characters
		self.matrix = np.empty([self.ntaxa, self.nchars], dtype=np.int8)

		taxon_index = 0
		# read in the characters
		for line in infile:
			if taxon_index == self.ntaxa:
				raise Exception("Too many taxa: " + str(taxon_index))

			data = re.split("(\t| {2,})", line)
			taxon_name = data[0]
			chars = data[2].strip()

			self.names[taxon_index] = taxon_name

			char_index = 0
			for char in chars:
				if char_index == self.nchars:
					raise Exception("Too many characters for taxon " + str(taxon_index))
				self.matrix[taxon_index, char_index] = int(char)
				char_index += 1

			taxon_index += 1

	def get_name(self, id):
		'''Return the name of a taxon with given id'''
		return self.names[id]

	def get_trait(self, taxon, char):
		'''Return the character state for a particular taxon'''
		return self.matrix[taxon, char]

	def print_me(self):
		'''Print information about the matrix'''
		print "Nchars: %d" % self.nchars
		print "Ntaxa: %d" % self.ntaxa
		print "Names:"
		print self.names
		print "Matrix:"
		print self.matrix

	def taxon_set(self):
		'''Return the set of taxa in the matrix'''
		return set(xrange(self.ntaxa))

	def get_outgroup(self):
		'''Return the id of the outgroup'''
		return 0

	def ingroup_set(self):
		'''Return the set of taxa in the ingroup'''
		return set(xrange(1, self.ntaxa))

def run_tests():
	cm = charmatrix("data/data.txt")

	# properties
	assert cm.nchars == 3, "matrix should have 3 characters"
	assert cm.ntaxa == 3, "matrix should have 3 taxa"

	# get_name
	assert cm.get_name(0) == 'A', "taxon id 0 should correspond to A"
	assert cm.get_name(1) == 'B', "taxon id 1 should correspond to B"

	# get_trait
	assert cm.get_trait(0, 0) == 0, "trait 0 should be 0 for A"
	assert cm.get_trait(1, 0) == 2, "trait 0 should be 2 for B"
	assert cm.get_trait(2, 1) == 0, "trait 1 should be 0 for C"

	# helper
	def list_of_set(s):
		return sorted(map(lambda id: cm.get_name(id), s))

	# taxon_set
	assert list_of_set(cm.taxon_set()) == ['A', 'B', 'C'], "taxa should be A, B, and C"

	# get_outgroup
	assert cm.get_name(cm.get_outgroup()) == 'A', "outgroup should be taxon A"

	# ingroup_set
	assert list_of_set(cm.ingroup_set()) == ['B', 'C'], "ingroup should be B and C"
