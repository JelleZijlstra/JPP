'''
Functionality for performing an algorithm like NNI in parallel.
'''

from mpi4py import MPI
import tree
import sys
import random
import time

TAG_FROM_MASTER_DIE = 1
TAG_GET_A_TREE = 2
TAG_GIVE_A_TREE = 3

class communicator(object):
	def __init__(self, cm, time_limit, communication_interval):
		self.cm = cm
		self.comm = MPI.COMM_WORLD
		self.comm_size = self.comm.Get_size()
		self.comm_rank = self.comm.Get_rank()
		self.is_master = self.comm_rank == 0

		current_time = time.time()
		self.time_limit = current_time + time_limit * 60
		self.communication_interval = communication_interval
		# initialize time to communicate first
		self.next_time = current_time + communication_interval
		if self.is_master:
			self.master_init()
		else:
			self.slave_init()

		# seed the PRNG differently in each process
		random.seed(self.comm_rank)

	def master_init(self):
		# initial send of trees
		#self.send_to_slaves(tree.one_tree(self.cm))
		pass

	def slave_init(self):
		pass

	def initial_tree(self):
		return tree.one_tree(cm)

	def send_to_slaves(self, tree, tag=TAG_GET_A_TREE):
		tree_list = self.stringify_list(tree)
		random.shuffle(tree_list)
		next_time = time.time() + self.communication_interval
		ntrees = len(tree_list)
		for i in xrange(1, self.comm_size):
			index = (i - 1) % ntrees
			self.comm.isend((tree_list[index:index + 1], next_time), dest=i, tag=tag)
		return next_time

	def master(self, t):
		# first, receive all the trees
		trees = set(t)
		for i in xrange(1, self.comm_size):
			for t in self.parse_list(self.comm.recv(source=i, tag=TAG_GIVE_A_TREE)):
				trees.add(t)
		fused = reduce(lambda x, y: x.fuse(y, self.cm), trees)
		trees.add(fused)
		best, best_len = tree.best(trees, self.cm)
		print "Number of best trees: ", len(best)
		print "Number of trees: ", len(trees)
		print "Number of input trees: ", len(t)
		if time.time() < self.time_limit:
			self.next_time = self.send_to_slaves(best)
			print "Current best tree length: %d" % best_len
			return best
		else:
			self.send_to_slaves(best, tag=TAG_FROM_MASTER_DIE)
			print "Final best tree length: %d" % best_len
			for t in best:
				print t.to_string(self.cm)
			sys.exit(0)

	@staticmethod
	def stringify_list(l):
		'''Turn a list of trees into a list of strings'''
		return map(lambda t: str(t), l)

	@staticmethod
	def parse_list(l):
		'''Turn a list of tree objects into a list of strings'''
		return map(lambda t: tree.parse(t), l)

	def slave(self, trees):
		'''Execute communication for the slave'''
		# send the tree to the master
		self.comm.isend(self.stringify_list(trees), dest=0, tag=TAG_GIVE_A_TREE)
		# and receive a tree back (from a previous iteration of the algorithm)
		status = MPI.Status()
		tree_str, next_time = self.comm.recv(source=0, status=status, tag=MPI.ANY_TAG)
		tag = status.Get_tag()
		if tag == TAG_FROM_MASTER_DIE:
			sys.exit(0)
		else:
			self.next_time = next_time
			return self.parse_list(tree_str)

	def callback(self, tree):
		'''Communicate with the other processes'''
		print "Executing callback: " + str(self.is_master)
		if self.is_master:
			return self.master(tree)
		else:
			return self.slave(tree)

	def need_to_communicate(self):
		'''Tell the process whether it needs to communicate its trees'''
		return time.time() > self.next_time
