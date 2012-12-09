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

def nni_search(cm, communicator):
	'''Perform a search using NNI'''
	first_tree = [tree.one_tree(cm)]
	first_len = first_tree[0].length(cm)
	print "Initial tree length: %d" % first_len
	i = 0
	while True:
		new_tree = rearrange_tree(first_tree[0])
		new_len = new_tree.length(cm)
		if new_len < first_len:
			print "New length, current minimum length: %d, %d" % (new_len, first_len)
			first_len = new_len
			first_tree = [new_tree]
		if i % 1000 == 0:
			communicator.callback(first_tree)
		i += 1
		random.shuffle(first_tree)

	return first_tree
