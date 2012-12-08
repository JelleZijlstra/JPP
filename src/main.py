'''Main entry point for the program'''

import charmatrix
import argparse

ALGORITHMS = ['exhaustive', 'bnb', 'branch-and-bound', 'nni', 'spr', 'tbr']

def main(args):
	if args.test:
		import run_tests
		run_tests.run()
	else:
		cm = charmatrix.charmatrix(args.datafile)

		if args.algorithm == 'exhaustive':
			import exhaustive
			tree = exhaustive.exhaustive_search(cm)
			print tree.to_string(cm)
		elif args.algorithm in ('bnb', 'branch-and-bound'):
			import branchnbound
			tree = branchnbound.branchnbound_search(cm)
			print tree.to_string(cm)
		else:
			import parallel_search
			comm = parallel_search.communicator(cm, args.time, args.interval)
			if args.algorithm == 'nni':
				import nni
				nni.nni_search(cm, comm)
			elif args.algorithm == 'spr':
				import spr
				spr.spr_search(cm, comm)
			elif args.algorithm == 'tbr':
				import tbr
				tbr.tbr_search(cm, comm)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Perform phylogenetic inference using maximum parsimony')

	parser.add_argument('--datafile', '-d', default='data/oryzos.txt', help='Data file to use as input')
	parser.add_argument('--algorithm', '-a', default='tbr', help='Algorithm to use for phylogenetic inference', choices=ALGORITHMS)
	parser.add_argument('--time', '-t', default=10, type=int, help='Maximum time to use (in minutes; only for heuristic algorithms)')
	parser.add_argument('--interval', '-i', default=10, type=int, help='Interval between communications between different MPI processes (in seconds)')
	parser.add_argument('--profile', '-p', default=False, help='Output profiling data using CProfile', action="store_true")
	parser.add_argument('--test', default=False, help='Whether to run tests', action="store_true")

	args = parser.parse_args()

	if args.profile:
		import cProfile
		cProfile.run('main(args)')
	else:
		main(args)

