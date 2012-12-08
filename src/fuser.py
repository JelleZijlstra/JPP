'''
Fuser - implement tree fusion

This is a technique for combining the good parts of different optimal or nearly
optimal trees. It detects subtrees in both trees that are similar and swaps in
the best one into the output trees.
'''

import tree

def unequal_fuse(t1, t2, cm):
	'''Fuse two subtrees containing potentially distinct sets of taxa. Return 
	two trees: one the optimal one including the taxa in t1, the other the 
	optimal one with taxa in t2'''
	t1set = t1.taxon_set()
	t2set = t2.taxon_set()
	if t1.is_terminal or t2.is_terminal or len(t1set & t2set) < 3:
		return t1, t2
	else:
		ll1, ll2 = unequal_fuse(t1.left, t2.left, cm)
		rr1, rr2 = unequal_fuse(t1.right, t2.right, cm)
		lr1, rl2 = unequal_fuse(t1.left, t2.right, cm)
		rl1, lr2 = unequal_fuse(t1.right, t2.left, cm)
		left = tree.one_best((tree.node(ll1, rr1), tree.node(ll1, rl1), tree.node(lr1, rr1), tree.node(lr1, rl1)), cm)
		right = tree.one_best((tree.node(ll2, rr2), tree.node(ll2, rl2), tree.node(lr2, rr2), tree.node(lr2, rl2)), cm)
		if t1set == t2set:
			best = tree.one_best((left, right), cm)
			return best, best
		else:
			return left, right

def fuse(t1, t2, cm):
	# left child of input tree will always be the outgroup
	return tree.node(t1.left, unequal_fuse(t1.right, t2.right, cm)[0])

def run_tests():
	import charmatrix
	cm = charmatrix.charmatrix('data/data3.txt')

	# Build two trees that are each optimal in one subtree
	t1 = tree.node(tree.leaf(0), tree.node(tree.leaf(1), tree.node(tree.node(tree.leaf(3), tree.node(tree.leaf(2), tree.leaf(4))), tree.node(tree.leaf(5), tree.node(tree.leaf(6), tree.leaf(7))))))
	t2 = tree.node(tree.leaf(0), tree.node(tree.leaf(1), tree.node(tree.node(tree.leaf(2), tree.node(tree.leaf(3), tree.leaf(4))), tree.node(tree.leaf(6), tree.node(tree.leaf(5), tree.leaf(7))))))
	optimal = tree.node(tree.leaf(0), tree.node(tree.leaf(1), tree.node(tree.node(tree.leaf(2), tree.node(tree.leaf(3), tree.leaf(4))), tree.node(tree.leaf(5), tree.node(tree.leaf(6), tree.leaf(7))))))
	fused = t1.fuse(t2, cm)
	# fusion should get the good parts out of both
	assert optimal == fused, "Fusion did not fuse optimally"
