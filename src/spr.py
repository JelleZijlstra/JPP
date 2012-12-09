'''
Subtree Pruning and Regrafting (SPR)

This is a heuristic algorithm that works as follows:
- Split an arbitrary subtree from the tree.
- Put it back in the tree at an arbitrary place.

The spr_searcher class is used to execute the algorithm; it is a
list_tree_searcher whose rearrange_tree method performs SPR.
'''

import list_tree
import random
from list_tree_searcher import list_tree_searcher

class spr_searcher(list_tree_searcher):
	def rearrange_tree(self):
		t = self.t
		node_count = t.node_count()
		# determine where to prune
		prune_index = random.randrange(node_count)
		if t.is_terminal(prune_index):
			t.prune_terminal(prune_index)
		else:
			# if it is not a terminal, determine where to put it back in
			child_index = t.tree[prune_index][random.randrange(3) + 1]
			if t.is_terminal(child_index):
				t.prune_terminal(child_index)
			else:
				t.debranch(prune_index, child_index)
				nodes = t.node_set(child_index, prune_index)
				nodes.add(prune_index)
				# make sure we don't regraft it within itself
				reattach_index = list_tree.random_not_in(node_count, nodes)
				t.regraft(child_index, prune_index, reattach_index)
		return t

def spr_search(cm, communicator):
	'''Perform a heuristic search using SPR'''
	searcher = spr_searcher(cm)
	communicator.do_search(searcher)
