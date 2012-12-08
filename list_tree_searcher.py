'''
Provides the abstract list_tree_searcher class, which performs a heuristic
search on list_tree objects by calling a subclass's rearrange_tree method.
'''

import list_tree
import copy

class list_tree_searcher(object):
	def __init__(self, cm, communicator):
		self.cm = cm
		self.communicator = communicator
		self.good_trees = []
		self.good_len = None

	def get_trees(self):
		'''Get the tree list in the form of tree (not list_tree) objects'''
		return map(lambda t: t.to_tree(), self.good_trees)

	def set_trees(self, trees):
		'''Set the tree list on the basis of a list of tree objects'''
		print "Current good length: %d" % self.good_len
		self.good_trees = map(lambda t: list_tree.list_tree(tree=t), trees)
		self.good_len = trees[0].length(self.cm)
		print "New good length: %d" % self.good_len

	def do_search(self):
		'''Perform a search'''
		cm = self.cm
		first_tree = list_tree.list_tree(taxa=cm.taxon_set(), outgroup=cm.get_outgroup())
		first_len = first_tree.length(cm)
		self.good_trees.append(first_tree)
		self.good_len = first_len

		print "Initial tree length: %d" % first_len
		while True:
			# perform rearrangements
			self.t = copy.deepcopy(self.good_trees[0])
			new_tree = self.rearrange_tree()
			new_len = new_tree.length(cm)

			# if they worked, expand our list of good trees
			if new_len < self.good_len:
				print "New length, current minimum length: %d, %d" % (new_len, self.good_len)
				self.good_len = new_len
				self.good_trees = [new_tree]
			elif new_len == self.good_len:
				self.good_trees.insert(0, new_tree)

			# perform communication with other processes
			if self.communicator.need_to_communicate():
				self.set_trees(self.communicator.callback(self.get_trees()))

		return self.good_trees
