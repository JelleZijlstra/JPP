import tree_parse

print tree_parse.parse('(1,2)')
print tree_parse.parse('((3,4),(2,3))')
print tree_parse.parse('((3,(4,5)),(1,2))')
