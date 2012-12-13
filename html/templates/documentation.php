<h2>Documentation</h2>
<p>The JPP program is a command-line Python script. Its input consists of textual data files and it outputs a list of optimal phylogenetic trees.</p>

<h3>Installation</h3>
<p>To install JPP, simply clone the Git repository:</p>
<div class="terminal-output">$ git clone git://github.com/JelleZijlstra/JPP.git</div>
<p>Pre-requisites are Python, MPI (for parallel processing) and the Python extensions numpy, CProfile, and mpi4py.</p>

<h3>Usage</h3>
<p>To run the program, navigate into the <tt>JP/src/</tt> directory. Usage of the program is as follows:</p>
<div class="terminal-output">
$ python main.py --help
usage: main.py [-h] [--datafile DATAFILE]
               [--algorithm {exhaustive,bnb,branch-and-bound,nni,spr,tbr,mixed}]
               [--time TIME] [--interval INTERVAL] [--profile] [--test]

Perform phylogenetic inference using maximum parsimony

optional arguments:
  -h, --help            show this help message and exit
  --datafile DATAFILE, -d DATAFILE
                        Data file to use as input
  --algorithm {exhaustive,bnb,branch-and-bound,nni,spr,tbr,mixed}, -a {exhaustive,bnb,branch-and-bound,nni,spr,tbr,mixed}
                        Algorithm to use for phylogenetic inference
  --time TIME, -t TIME  Maximum time to use (in minutes; only for heuristic
                        algorithms)
  --interval INTERVAL, -i INTERVAL
                        Interval between communications between different MPI
                        processes (in seconds)
  --profile, -p         Output profiling data using CProfile
  --test                Run tests
</div>
