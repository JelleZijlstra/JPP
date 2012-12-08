'''
Class representing a phylogenetic tree

type tree =
	Leaf of int
	| Node of tree * tree
;;

Trees are IMMUTABLE. Even though they can't really be in Python.

'''

import numpy as np
import fuser
import tree_parse

class tree(object):
	def __init__(self, id=None, children=None):
		self.is_terminal = children == None
		if self.is_terminal:
			self.id = id
		else:
			self.left, self.right = children
		self.length_cache = None
		self.size_cache = None
		self.left_first = True

	def children(self):
		'''Returns the left and right sub-trees, in pseudo-random order'''
		if self.left_first:
			out = self.left, self.right
		else:
			out = self.right, self.left
		self.left_first = not self.left_first
		return out

	def length(self, cm):
		total = 0
		lengths = self.char_length(cm)
		for i in xrange(cm.nchars):
			traits, length = lengths[i]
			total += length
		return total

	# http://ab.inf.uni-tuebingen.de/teaching/ws06/albi1/script/phylogeny_31Jan2007.pdf
	def char_length(self, cm):
		if self.length_cache == None:
			length = np.empty(cm.nchars, dtype=np.object_)
			if self.is_terminal:
				for i in xrange(cm.nchars):
					length[i] = set([cm.get_trait(self.id, i)]), 0
			else:
				l, r = self.left.char_length(cm), self.right.char_length(cm)
				for i in xrange(cm.nchars):
					l_set, l_len = l[i]
					r_set, r_len = r[i]
					inter = l_set & r_set
					if len(inter) == 0:
						length[i] = (l_set | r_set, l_len + r_len + 1)
					else:
						length[i] = (inter, l_len + r_len)
			self.length_cache = length
			return length
		else:
			return self.length_cache

	def to_string(self, cm):
		if self.is_terminal:
			return str(cm.get_name(self.id))
		else:
			return '(' + self.left.to_string(cm) + ',' + self.right.to_string(cm) + ')'		

	def size(self):
		'''Return the number of leaves in the tree'''
		if self.size_cache != None:
			return self.size_cache
		else:
			if self.is_terminal:
				size = 1
			else:
				size = self.left.size() + self.right.size()
			self.size_cache = size
			return size

	def __str__(self):
		if self.is_terminal:
			return str(self.id)
		else:
			return '(' + str(self.left) + ',' + str(self.right) + ')'

	def all_trees_left(self, l):
		'''Return all trees with the left child being an element in l and the right child being self'''
		return (tree(children=(elt, self)) for elt in l)

	def all_trees_right(self, l):
		'''Return all trees with the left child being self and the right child being an element in l'''
		return (tree(children=(self, elt)) for elt in l)

	def trees_adding(self, taxon):
		'''Return all the trees that can be obtained from adding taxon to the tree t'''
		if self.is_terminal:
			return [tree(children=(self, tree(id=taxon)))]
		else:
			l, r = self.left, self.right
			return flatten([[tree(children=(self, tree(id=taxon)))], \
				r.all_trees_left(l.trees_adding(taxon)), \
				l.all_trees_right(r.trees_adding(taxon))])

	def __eq__(self, rhs):
		if self.is_terminal != rhs.is_terminal:
			return False
		elif self.is_terminal:
			return self.id == rhs.id
		else:
			return (self.left == rhs.left) and (self.right == rhs.right)

	def taxon_set(self):
		if self.is_terminal:
			return set([self.id])
		else:
			return self.left.taxon_set() | self.right.taxon_set()

	def fuse(self, rhs, cm):
		return fuser.fuse(self, rhs, cm)

	def __hash__(self):
		return hash(str(self))

def node(l, r):
	'''Sugar for tree.tree(children=(l, r))'''
	return tree(children=(l, r))

def leaf(id):
	'''Sugar for tree.tree(id=id)'''
	return tree(id=id)

def flatten(l):
	'''From a generator returning generators returning items, create a generator directly returning the items'''
	return (item for sublist in l for item in sublist)

def all_trees_rec(taxa):
	'''Return all the trees that can be made out of the set of taxa taxa, recursively. The recursive implementation was necessary because otherwise taxon was not scoped correctly.'''
	if len(taxa) == 1:
		return [tree(id=taxa.pop())]
	else:
		taxon = taxa.pop()
		return flatten((t.trees_adding(taxon) for t in all_trees_rec(taxa)))

def all_trees(taxa, outgroup):
	'''Return all trees that can be made from taxa'''
	taxa.remove(outgroup)
	outgroup_tree = tree(id=outgroup)
	return (tree(children=(outgroup_tree, t)) for t in all_trees_rec(taxa))

def one_tree(cm):
	'''Return a single tree with all the taxa in the matrix'''
	outgroup = cm.get_outgroup()
	taxa = cm.ingroup_set()
	out_tree = tree(id=taxa.pop())
	for taxon in taxa:
		out_tree = tree(children=(tree(id=taxon), out_tree))
	return tree(children=(tree(id=outgroup), out_tree))

def best(trees, cm):
	best_trees = []
	best_length = None
	for tree in trees:
		tree_len = tree.length(cm)
		if best_length == None or tree_len < best_length:
			best_length = tree_len
			best_trees = [tree]
		elif tree_len == best_length:
			best_trees.append(tree)
	return best_trees, best_length

def one_best(trees, cm):
	best_trees, length = best(trees, cm)
	return best_trees[0]

def parse(string):
	return tree_parse.parse(string)
