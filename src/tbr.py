'''
Tree Bissection-Reconnection (TBR)

A heuristic algorithm that splits an unrooted tree into two at an arbitrary
node, then re-joins them at arbitrary nodes.

This is equivalent to SPR when some of the nodes involved are terminals.
'''

import list_tree
import random
from list_tree_searcher import list_tree_searcher

class tbr_searcher(list_tree_searcher):
	def rearrange_tree(self):
		t = self.t
		node_count = t.node_count()
		prune_index = random.randrange(node_count)
		if t.is_terminal(prune_index):
			t.prune_terminal(prune_index)
		else:
			child_index = t.tree[prune_index][random.randrange(3) + 1]
			if t.is_terminal(child_index):
				t.prune_terminal(child_index)
			else:
				nodes = t.node_set(child_index, prune_index)
				nodes.add(prune_index)
				t.debranch(prune_index, child_index)
				t.debranch(child_index, prune_index)
				reattach_index_one = list_tree.random_not_in(node_count, nodes)

				nodes.remove(prune_index)
				nodes.remove(child_index)
				reattach_index_two = list_tree.random_in(node_count, nodes)
				t.regraft(child_index, prune_index, reattach_index_one)
				t.regraft(prune_index, child_index, reattach_index_two)
		return t

def tbr_search(cm, communicator):
	searcher = tbr_searcher(cm)
	communicator.do_search(searcher)
