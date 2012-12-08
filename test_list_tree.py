import sys
import list_tree
import tree
import charmatrix

cm = charmatrix.charmatrix('data/shortoryzos.txt')
t = tree.one_tree(cm)

print t
lt = list_tree.list_tree(tree=t)
tt = lt.to_tree()
print tt
print t.length(cm)
print lt.length(cm)
