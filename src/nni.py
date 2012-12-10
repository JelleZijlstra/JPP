'''
Nearest Neighbor Interchange (NNI)

A heuristic algorithm that makes local changes to the tree. For example, it may
change a tree of the form:
	((1,2),(3,4))
to:
	(1,(2,(3,4)))
'''

import tree
import random

def do_rearrange(t):
	'''Perform a rearrangement on a tree'''
	if t.left.is_terminal:
		child1, child2 = t.right, t.left
	elif t.right.is_terminal:
		child1, child2 = t.left, t.right
	else:
		child1, child2 = t.children()

	gchild1, gchild2 = child1.children()
	return tree.tree(children=(gchild1, tree.tree(children=(gchild2, child2))))

def rearrange_tree(t):
	'''Take a tree, and rearrange either a tree or a child. Return the rearranged tree.'''
	if t.size() == 3:
		return do_rearrange(t)
	lsize = t.left.size()
	rsize = t.right.size()
	if lsize < 3 and rsize < 3:
		return do_rearrange(t)
	elif lsize < 3:
		rand = random.randrange(rsize - 1)
		if rand == 0:
			return do_rearrange(t)
		else:
			return tree.tree(children=(t.left, rearrange_tree(t.right)))
	elif rsize < 3:
		rand = random.randrange(lsize - 1)
		if rand == 0:
			return do_rearrange(t)
		else:
			return tree.tree(children=(rearrange_tree(t.left), t.right))
	else:
		rand = random.randrange(lsize + rsize - 3)
		if rand == 0:
			return do_rearrange(t)
		elif rand < lsize - 1:
			return tree.tree(children=(rearrange_tree(t.left), t.right))
		else:
			return tree.tree(children=(t.left, rearrange_tree(t.right)))

class nni_searcher(object):
	def __init__(self, cm):
		self.cm = cm

	def do_search(self, comm, trees=None):
		cm = self.cm
		if trees == None:
			first_tree = [tree.one_tree(cm)]
			first_len = first_tree[0].length(cm)
			print "Initial tree length: %d" % first_len
		else:
			first_tree = trees
			first_len = trees[0].length(cm)

		while not comm.need_to_communicate():
			# preserve outgroup
			t = first_tree[0]
			new_tree = tree.node(t.left, rearrange_tree(t.right))
			new_len = new_tree.length(cm)
			if new_len < first_len:
				print "New length, current minimum length: %d, %d" % (new_len, first_len)
				first_len = new_len
				first_tree = [new_tree]
			elif new_len == first_len:
				first_tree.append(new_tree)

			random.shuffle(first_tree)

		# commmunicate back
		return first_tree

def nni_search(cm, communicator):
	'''Perform a search using NNI'''
	searcher = nni_searcher(cm)
	communicator.do_search(searcher)
