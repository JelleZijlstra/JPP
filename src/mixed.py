'''
Mixed search
Perform a different 

'''

import nni
import spr
import tbr

ALGORITHMS = [tbr, spr, nni]

from mpi4py import MPI

class mixed_searcher(object):
	def __init__(self, cm):
		self.cm = cm
		comm = MPI.COMM_WORLD
		n_algos = len(ALGORITHMS)
		index = comm.Get_rank() % n_algos
		self.searcher = ALGORITHMS[index].searcher(cm)

	def do_search(self, comm, trees=None):
		return self.searcher.do_search(comm, trees=trees)

def mixed_search(cm, communicator):
	searcher = mixed_searcher(cm)
	communicator.do_search(searcher)
