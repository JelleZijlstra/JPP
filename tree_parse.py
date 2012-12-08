'''
Parse a string into a tree

This is the grammar in a simplied form:

program:
	tree
;

tree:
	leaf
	| '(' tree ',' tree ')'
;

leaf:
	\d+
;

This parser was constructed on the basis of the parser constructed by Yacc from the grammar in dev/tree.y.

'''
import tree

INT_RANGE = range(ord('0'), ord('9') + 1)

T_DIGIT = 258
T_END = 259

def tokenize(string):
	current_number = ''
	for c in string:
		if c in ('(', ',', ')'):
			if current_number != '':
				yield T_DIGIT, int(current_number)
				current_number = ''
			yield c, c
		elif ord(c) in INT_RANGE:
			current_number += c
		else:
			raise SyntaxError("Unexpected character: " + c)
	yield T_END, T_END

class parser(object):
	def __init__(self, string):
		self.stream = tokenize(string)
		self.state_stack = [0]
		self.parse_stack = []
		self.lookahead = None
		self.content = None

	def print_state(self):
		print "STATE"
		print self.state_stack
		print [str(t) for t in self.parse_stack]
		print self.lookahead
		print self.content

	def shift(self):
		try:
			self.lookahead, self.content = next(self.stream)
		except StopIteration:
			self.lookahead, self.content = None, None

	def current_state(self):
		return self.state_stack[-1]

	def goto(self, n):
		self.state_stack.append(n)

	def reduce(self, rule):
		if rule == 1:
			self.result = self.parse_stack.pop()
		elif rule == 2:
			digit = self.parse_stack.pop()
			self.parse_stack.append(tree.leaf(digit))
		elif rule == 3:
			r = self.parse_stack.pop()
			l = self.parse_stack.pop()
			# this rule has 
			self.state_stack.pop()
			self.state_stack.pop()
			self.state_stack.pop()
			self.state_stack.pop()
			self.parse_stack.append(tree.node(l, r))
		self.state_stack.pop()
		state = self.current_state()
		if state == 0:
			if rule == 1:
				self.goto(3)
			elif rule == 2 or rule == 3:
				self.goto(4)
		elif state == 2:
			self.goto(5)
		elif state == 7:
			self.goto(8)

	def do_parse(self):
		self.shift()
		while True:
			#self.print_state()
			state = self.current_state()
			if state == 0 or state == 2 or state == 7:
				if self.lookahead == T_DIGIT:
					self.parse_stack.append(self.content)
					self.shift()
					self.goto(1)
				elif self.lookahead == '(':
					self.shift()
					self.goto(2)
				else:
					raise SyntaxError("Unexpected " + str(self.lookahead))
			elif state == 1:
				self.reduce(2)
			elif state == 3:
				if self.lookahead == T_END:
					self.shift()
					self.goto(6)
				else:
					raise SyntaxError("Unexpected " + str(self.lookahead))
			elif state == 4:
				self.reduce(1)
			elif state == 5:
				if self.lookahead == ',':
					self.shift()
					self.goto(7)
				else:
					raise SyntaxError("Unexpected " + str(self.lookahead))
			elif state == 6:
				return self.result
			elif state == 8:
				if self.lookahead == ')':
					self.shift()
					self.goto(9)
				else:
					raise SyntaxError("Unexpected " + str(self.lookahead))
			elif state == 9:
				self.reduce(3)

def parse(string):
	p = parser(string)
	return p.do_parse()

def run_tests():
	node = tree.node
	leaf = tree.leaf

	# test the tokenizer
	tokens = list(tokenize('(1,2)'))
	assert tokens == [('(', '('), (T_DIGIT, 1), (',', ','), (T_DIGIT, 2), (')', ')'), (T_END, T_END)], "tokenizer does not run correctly"

	# test the whole parsing process
	t1 = parse('(1,2)')
	assert t1 == node(leaf(1), leaf(2)), "cannot parse simple tree"
	t2 = parse('((3,4),(2,1))')
	assert t2 == node(node(leaf(3), leaf(4)), node(leaf(2), leaf(1))), "cannot parse tree of depth 2"
	t3 = parse('((3,(4,5)),(1,2))')
	assert t3 == node(node(leaf(3), node(leaf(4), leaf(5))), node(leaf(1), leaf(2))), "cannot parse tree of depth 3"

