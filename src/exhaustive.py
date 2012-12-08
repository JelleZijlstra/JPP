'''
Exhaustive search

Algorithm:
- Start with the single tree that contains one taxon
- Add the next taxon on every possible spot in the tree (i.e., sister to every node or terminal)
- Repeat until all taxa are added
- Then evaluate the trees
'''

import serial_util
import tree

def exhaustive_search(cm):
	'''Do an exhaustive search on all possible trees in the char matrix'''
	taxa = cm.taxon_set()
	outgroup = cm.get_outgroup()

	trees = tree.all_trees(taxa, outgroup)

	best_tree = None
	best_length = None
	ntrees = 0
	for a_tree in trees:
		ntrees += 1
		tree_len = a_tree.length(cm)
		if best_length == None or tree_len < best_length:
			best_tree = a_tree
			best_length = tree_len

	print "Total trees examined: %d" % ntrees
	print "Length of best tree: %d" % best_length

	return best_tree

def run_tests():
	import charmatrix
	cm = charmatrix.charmatrix("data/data2.txt")
	t = exhaustive_search(cm)
	assert t == tree.parse("(0,(1,(2,(3,4))))"), "exhaustive search must return this tree"
