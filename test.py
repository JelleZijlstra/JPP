import tree
import charmatrix
import serial_util

node = tree.node
leaf = tree.leaf

cm = charmatrix.charmatrix('data3.txt')

t1 = node(leaf(0), node(leaf(1), node(node(leaf(3), node(leaf(2), leaf(4))), node(leaf(5), node(leaf(6), leaf(7))))))
print "t1: " + t1.to_string(cm)

t2 = node(leaf(0), node(leaf(1), node(node(leaf(2), node(leaf(3), leaf(4))), node(leaf(6), node(leaf(5), leaf(7))))))
print "t2: " + t2.to_string(cm)

optimal = node(leaf(0), node(leaf(1), node(node(leaf(2), node(leaf(3), leaf(4))), node(leaf(5), node(leaf(6), leaf(7))))))
print "Optimal: " + optimal.to_string(cm)

def runner():
	return t1.fuse(t2, cm)

fused, time = serial_util.time_serial(runner, label="Fusion")
print "Fused: " + fused.to_string(cm)
assert optimal == fused
