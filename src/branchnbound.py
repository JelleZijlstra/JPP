'''
Branch-and-bound search

Similar to exhaustive search, but immediately discards those trees that have a
length greater than the length of the shortest tree found so far.

This is an exact method and has bad, possibly O(n!), time complexity.
'''

import serial_util
import tree

best_length = None

def trees_adding_bb(t, taxon, cm, og):
	'''Yield all the trees that can be obtained from adding taxon to the tree t'''
	new_tree = tree.tree(children=(t, tree.tree(id=taxon)))
	if best_length == None or tree.tree(children=(og, new_tree)).length(cm) < best_length:
		yield new_tree

	if not t.is_terminal:
		l, r = t.left, t.right
		for a_tree in r.all_trees_left(trees_adding_bb(l, taxon, cm, og)):
			yield a_tree
		for a_tree in l.all_trees_right(trees_adding_bb(r, taxon, cm, og)):
			yield a_tree

def all_trees_rec_bb(taxa, cm, og):
	'''Return all the trees that can be made out of the set of taxa taxa,
	recursively. The recursive implementation was necessary because otherwise
	taxon was not scoped correctly.'''
	if len(taxa) == 1:
		return [tree.tree(id=taxa.pop())]
	else:
		taxon = taxa.pop()
		trees = (trees_adding_bb(t, taxon, cm, og) for t in all_trees_rec_bb(taxa, cm, og))
		return tree.flatten(trees)

def branchnbound_search(cm):
	'''Do an exhaustive search on all possible trees in the char matrix using
	branch-and-bound methods.'''
	global best_length
	taxa = cm.taxon_set()
	outgroup = cm.get_outgroup()
	taxa.remove(outgroup)
	outgroup_tree = tree.tree(id=outgroup)

	trees = all_trees_rec_bb(taxa, cm, outgroup_tree)

	best_tree = None
	ntrees = 0
	for a_tree in trees:
		ntrees += 1
		real_tree = tree.tree(children=(outgroup_tree, a_tree))
		tree_len = real_tree.length(cm)
		if best_length == None or tree_len < best_length:
			best_tree = [real_tree]
			best_length = tree_len
		elif tree_len == best_length:
			best_tree.append(real_tree)

	print "Total trees examined: %d" % ntrees
	print "Length of best tree(s): %d" % best_length	
	print "Number of best tree(s): %d" % len(best_tree)

	return best_tree
