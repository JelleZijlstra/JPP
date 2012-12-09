import nni
import spr
import tbr

from mpi4py import MPI

class mixed_searcher(object):
	def __init__(self, cm):
		self.cm = cm
		comm = MPI.COMM_WORLD
		index = comm.Get_rank() % 3
		if index == 0:
			self.searcher = tbr.tbr_searcher(cm)
		elif index == 1:
			self.searcher = spr.spr_searcher(cm)
		elif index == 2:
			self.searcher = nni.nni_searcher(cm)

	def do_search(self, comm, trees=None):
		return self.searcher.do_search(comm, trees=trees)

def mixed_search(cm, communicator):
	searcher = mixed_searcher(cm)
	communicator.do_search(searcher)
