'''Main entry point for the program'''

import charmatrix
import exhaustive
import branchnbound
import nni
import spr
import tbr
import parallel_search

import argparse

ALGORITHMS = ['exhaustive', 'bnb', 'branch-and-bound', 'nni', 'spr', 'tbr']

DO_PROFILE = True

def main():
	parser = argparse.ArgumentParser(description='Perform phylogenetic inference using maximum parsimony')

	parser.add_argument('--datafile', '-d', default='data/oryzos.txt', help='Data file to use as input')
	parser.add_argument('--algorithm', '-a', default='tbr', help='Algorithm to use for phylogenetic inference', choices=ALGORITHMS)
	parser.add_argument('--time', '-t', default=10, type=int, help='Maximum time to use (in minutes; only for heuristic algorithms)')
	parser.add_argument('--interval', '-i', default=10, type=int, help='Interval between communications between different MPI processes (in seconds)')

	args = parser.parse_args()

	cm = charmatrix.charmatrix(args.datafile)

	if args.algorithm == 'exhaustive':
		tree = exhaustive.exhaustive_search(cm)
		print(tree.to_string(cm))
	elif args.algorithm in ('bnb', 'branch-and-bound'):
		tree = branchnbound.branchnbound_search(cm)
		print tree.to_string(cm)
	else:
		comm = parallel_search.communicator(cm, args.time, args.interval)
		if args.algorithm == 'nni':
			nni.nni_search(cm, comm)
		elif args.algorithm == 'spr':
			spr.spr_search(cm, comm)
		elif args.algorithm == 'tbr':
			tbr.tbr_search(cm, comm)

if __name__ == '__main__':
	if DO_PROFILE:
		import cProfile
		cProfile.run('main()')
	else:
		main()

