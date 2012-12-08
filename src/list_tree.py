'''
list_tree: implement unrooted trees using a list

A list_tree's tree is represented in self.tree, which is a list of tuples that can take two forms:
- (int : id * int : index), representing a terminal node's id plus the index of its parent node
- (None, int : index * int : index * int : index), representing the three neighbors of an internal node
'''

import random
import tree

class list_tree(object):
	def __init__(self, taxa=None, outgroup=None, tree=None):
		if outgroup != None:
			self.init_from_taxa(taxa, outgroup)
		else:
			self.init_from_tree(tree)

	def init_from_taxa(self, taxa, outgroup):
		'''Create a random tree from a set of taxa'''
		self.outgroup = outgroup
		taxon_list = list(taxa)
		random.shuffle(taxon_list)
		self.outgroup_index = taxon_list.index(outgroup)
		self.ntaxa = len(taxon_list)
		self.tree = [(taxon, None) for taxon in taxon_list]
		first_loose = 0
		total_loose = self.ntaxa
		tree_length = self.ntaxa
		while tree_length - first_loose > 3:
			# give the loose ones a parent
			self.give_parent(first_loose, tree_length)
			self.give_parent(first_loose + 1, tree_length)
			# add new node
			self.tree.append((None, first_loose, first_loose + 1, None))
			# update variables
			first_loose += 2
			tree_length += 1
		self.give_parent(first_loose, tree_length)
		self.give_parent(first_loose + 1, tree_length)
		self.give_parent(first_loose + 2, tree_length)
		self.tree.append((None, first_loose, first_loose + 1, first_loose + 2))

	def init_from_tree(self, t):
		'''Construct a list_tree from a tree object'''
		# manually construct first few nodes
		self.outgroup = t.left.id
		self.outgroup_index = 0
		self.tree = [(self.outgroup, 1)]
		self.init_from_tree_rec(t.right, 0)

	def init_from_tree_rec(self, t, parent_index):
		'''Build up the list_tree from a tree, recursively'''
		if t.is_terminal:
			self.tree.append((t.id, parent_index))
			return len(self.tree) - 1
		else:
			self.tree.append(None)
			my_index = len(self.tree) - 1
			left_child = self.init_from_tree_rec(t.left, my_index)
			right_child = self.init_from_tree_rec(t.right, my_index)
			self.tree[my_index] = (None, parent_index, left_child, right_child)
			return my_index

	def give_parent(self, index, parent):
		'''Give the node at index index the parent parent'''
		if self.is_terminal(index):
			self.tree[index] = self.tree[index][0], parent
		else:
			existing = self.tree[index]
			self.tree[index] = existing[0], existing[1], existing[2], parent

	def is_terminal(self, index):
		'''Determine whether the node at index index is a terminal'''
		length = len(self.tree[index])
		if length == 2:
			return True
		elif length == 4:
			return False
		else:
			assert False

	def to_tree(self):
		'''Convert this object into a tree object'''
		outgroup, initial_pointer = self.tree[self.outgroup_index]
		return tree.node(tree.leaf(outgroup), self.to_tree_rec(initial_pointer, self.outgroup_index))

	def to_tree_rec(self, node_index, parent_index):
		'''Recursive helper for converting a subtree into a tree object'''
		if self.is_terminal(node_index):
			taxon_id, parent = self.tree[node_index]
			assert parent == parent_index
			return tree.leaf(taxon_id)
		else:
			children = list(self.tree[node_index][1:])
			children.remove(parent_index)
			left_child = self.to_tree_rec(children[0], node_index)
			right_child = self.to_tree_rec(children[1], node_index)
			return tree.node(left_child, right_child)

	def children_without(self, index, parent):
		'''Return an internal node's neighbors except for parent'''
		children = list(self.tree[index][1:])
		children.remove(parent)
		return children[0], children[1]		

	def length(self, cm):
		'''Calculate the length of this tree'''
		root_index = self.tree[self.outgroup_index][1]
		total_length = 0
		for i in xrange(cm.nchars):
			char_set, length = self.char_length(cm, root_index, i, self.outgroup_index)
			if cm.get_trait(self.outgroup, i) not in char_set:
				length += 1
			total_length += length
		return total_length

	def char_length(self, cm, index, char, parent):
		'''Calculate tree length for a single character, recursively'''
		if self.is_terminal(index):
			return set([cm.get_trait(self.tree[index][0], char)]), 0
		else:
			l, r = self.children_without(index, parent)
			l_set, l_len = self.char_length(cm, l, char, index)
			r_set, r_len = self.char_length(cm, r, char, index)
			inter = l_set & r_set
			if len(inter) == 0:
				return l_set | r_set, l_len + r_len + 1
			else:
				return inter, l_len + r_len

	def node_set(self, node, parent):
		'''Calculate the set of nodes in this tree'''
		if self.is_terminal(node):
			return set([node])
		else:
			l, r = self.children_without(node, parent)
			my_set = self.node_set(l, node) | self.node_set(r, node)
			my_set.add(node)
			return my_set

	def node_count(self):
		'''Return the number of nodes (internal and terminal) in the tree'''
		return len(self.tree)

	def replace_parent(self, change_in, change_from, change_to):
		'''Replace one of the connecting nodes of node change_in from change_from to change_to'''
		if self.is_terminal(change_in):
			leaf_id, current_parent = self.tree[change_in]
			assert current_parent == change_from
			self.tree[change_in] = leaf_id, change_to
		else:
			l, r = self.children_without(change_in, change_from)
			self.tree[change_in] = None, l, r, change_to

	def debranch(self, node, parent):
		'''Detach this node from the tree'''
		grandpa, grandma = self.children_without(node, parent)
		self.replace_parent(grandpa, node, grandma)
		self.replace_parent(grandma, node, grandpa)

	def regraft(self, pruned, empty_node, at):
		'''Put the node with root at pruned back into tree t at position at, using
		the node empty_node for the connection'''
		if self.is_terminal(at):
			at_parent = self.tree[at][1]
			self.replace_parent(at_parent, at, empty_node)
			self.replace_parent(at, at_parent, empty_node)
			self.tree[empty_node] = (None, pruned, at_parent, at)
		else:
			child_index = random.randrange(3) + 1
			new_sibling = self.tree[at][child_index]
			self.replace_parent(at, new_sibling, empty_node)
			self.replace_parent(new_sibling, at, empty_node)
			self.tree[empty_node] = (None, pruned, new_sibling, at)

	def prune_terminal(self, prune_index):
		'''Prune and regraft a terminal node'''
		# first, prune the terminal out of the tree
		node_to_change = self.tree[prune_index][1]
		self.debranch(node_to_change, prune_index)
		# then, reattach it
		reattach_index = random_not_in(self.node_count(), (prune_index, node_to_change))
		self.regraft(prune_index, node_to_change, reattach_index)

def random_not_in(size, not_in):
	'''Return a random number smaller than size that is not in not_in'''
	out = random.randrange(size)
	while out in not_in:
		out = (out + 1) % size
	return out

def random_in(size, in_set):
	'''Return a random number smaller than size that is in in_set'''
	out = random.randrange(size)
	while out not in in_set:
		out = (out + 1) % size
	return out

def run_tests():
	# random_not_in
	my_set = set([1, 2, 3, 4])
	assert random_not_in(5, my_set) == 0, "it can only be 0"
	# random_in
	assert random_in(5, my_set) in my_set, "number must be in set"

	# list_tree itself
	import charmatrix

	# prepare trees
	cm = charmatrix.charmatrix('data/shortoryzos.txt')
	t = tree.one_tree(cm)

	# test conversion with tree
	lt = list_tree(tree=t)
	tt = lt.to_tree()
	assert tt == t, "list_tree <=> tree conversion should be reversible"

	# test length
	assert t.length(cm) == lt.length(cm), "tree length should give same result for tree and list_tree"

	# test init_from_taxa
	taxa = cm.taxon_set()
	outgroup = cm.get_outgroup()
	lt2 = list_tree(taxa=taxa, outgroup=outgroup)
	assert lt2.to_tree().taxon_set() == taxa
