<h2>Documentation</h2>
<p>The JPP program is a command-line Python script. Its input consists of textual data files and it outputs a list of optimal phylogenetic trees.</p>

<h3>Installation</h3>
<p>To install JPP, simply clone the Git repository:</p>
<div class="terminal-output">$ git clone git://github.com/JelleZijlstra/JPP.git</div>
<p>Pre-requisites are Python, MPI (for parallel processing) and the Python extensions numpy, CProfile, and mpi4py.</p>

<h3>Usage</h3>
<p>To run the program, navigate into the <tt>JPP/src/</tt> directory. Usage of the program is as follows:</p>
<div class="terminal-output">$ python main.py --help
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

<h3>Datafiles</h3>
<p>Datafiles must contain a table with names of terminal taxa (e.g., species included in the phylogenetic analysis), followed by whitespace, followed by a listing of the taxon's state for each character included. Above the table must be a line containing the number of characters and the number of taxa. All line starting with <tt>#</tt> are ignored.</p>

<p>The following is an example datafile:</p>
<div class="terminal-output">$ cat data/data.txt 
# Very simple datafile.
3 3
A 012
B 210
C 000
</div>
<p>This datafile lists three taxa, named A, B, and C, and three characters. For the first character, taxa A and C have state 0 while B has state 2; for the second A and B have state 1 while C has 0; and for the third A has 2 while B and C have 0.</p>

<p>The <tt>JPP/src/data/</tt> directory contains some further examples of datafiles.</p>

<h3>Algorithms and parallel processing</h3>
<p>The algorithm is specified using the <tt>-a</tt> command-line option. Options are:</p>
<ul>
	<li><tt>exhaustive</tt> – perform an exhaustive search</li>
	<li><tt>bnb</tt> / <tt>branch-and-bound</tt> – perform branch-and-bound search (an exact algorithm that is slightly more efficient than exhaustive search)</li>
	<li><tt>nni</tt> – perform a heuristic search using the NNI algorithm</li>
	<li><tt>spr</tt> – heuristic search using SPR</li>
	<li><tt>tbr</tt> – heuristic search using TBR</li>
	<li><tt>mixed</tt> – heuristic search using NNI, SPR, and TBR in different processes</li>
</ul>
<p>Below is an example program output using exhaustive search:</p>
<div class="terminal-output">$ python main.py -a exhaustive -d data/data3.txt 
Character matrix has 11 characters for 8 taxa
Total trees examined: 10395
Length of best tree(s): 11
Number of best tree(s): 3
(A,(B,((C,(D,E)),(F,(G,H)))))
(A,((B,(C,(D,E))),(F,(G,H))))
(A,((B,(F,(G,H))),(C,(D,E))))
</div>

<p>The <tt>exhaustive</tt> and <tt>bnb</tt> algorithms can only be run serially. The other algorithms can be run in parallel using MPI (and in the case of <tt>mixed</tt>, this is essential to the algorithm). Parallelism is implemented by having the different processes execute a heuristic algorithm independently for a period specified by the <tt>-t</tt> command-line option. After an interval specified by the <tt>-i</tt> command-line options, the processes communicate with each other and the master process finds the best tree among the ones generated by the different processes. It sends this tree back to the other processes, which then continue their heuristic search. See <a href="design.php">Design</a> for details on the implementation of these algorithsm.</p>

<p>The below is example output when running four MPI processes using TBR:</p>
<div class="terminal-output scrollable">$ openmpirun -n 4 python main.py -t 1 -i 15 -d data/data3.txt -a tbr
Character matrix has 11 characters for 8 taxa
Character matrix has 11 characters for 8 taxa
Character matrix has 11 characters for 8 taxa
Character matrix has 11 characters for 8 taxa
Initial tree length: 19
Initial tree length: 20
New length, current minimum length: 19, 20
Initial tree length: 16
Initial tree length: 20
New length, current minimum length: 16, 20
New length, current minimum length: 17, 19
New length, current minimum length: 18, 19
New length, current minimum length: 15, 16
New length, current minimum length: 14, 18
New length, current minimum length: 15, 17
New length, current minimum length: 14, 15
New length, current minimum length: 14, 16
New length, current minimum length: 12, 14
New length, current minimum length: 13, 14
New length, current minimum length: 12, 13
New length, current minimum length: 12, 14
New length, current minimum length: 11, 12
New length, current minimum length: 11, 12
New length, current minimum length: 13, 15
New length, current minimum length: 11, 12
New length, current minimum length: 12, 13
New length, current minimum length: 11, 12
Executing callback: Master
Executing callback: Slave
Executing callback: Slave
Executing callback: Slave
Current best tree length: 11
Current good length: 11
Current good length: 11
New good length: 11
Current good length: 11
New good length: 11
New good length: 11
Current good length: 11
New good length: 11
Executing callback: Slave
Executing callback: Master
Executing callback: Slave
Executing callback: Slave
Current best tree length: 11
Current good length: 11
Current good length: 11
Current good length: 11
New good length: 11
New good length: 11
New good length: 11
Current good length: 11
New good length: 11
Executing callback: Slave
Executing callback: Master
Executing callback: Slave
Executing callback: Slave
Current best tree length: 11
Current good length: 11
Current good length: 11
New good length: 11
Current good length: 11
New good length: 11
New good length: 11
Current good length: 11
New good length: 11
Executing callback: Master
Executing callback: Slave
Executing callback: Slave
Executing callback: Slave
Final best tree length: 11
(A,((B,(C,(D,E))),(F,(G,H))))
(A,((B,(F,(G,H))),(C,(D,E))))
(A,(B,((C,(D,E)),(F,(G,H)))))
</div>

<p>The processes print progress information when they find a better tree and when communicating with the master. In this case, the use of multiple processes is overkill; all four processes independently found at least one of the best trees before the first communication.</p>

<h3>Other options</h3>
<p>When invoked with the <tt>--test</tt> option, <tt>main.py</tt> will run unit tests for some portions of the program (other options are ignored). When invoked with <tt>--profile</tt>, the CProfile Python extension is used to profile the execution of the Python code.</p>

<h3>JavaScript implementation</h3>
<p>I re-implemented a small portion of the project in JavaScript. The JavaScript code (in <a href="tree/tree.js">tree.js</a>) implements exhaustive search and a function to display trees dynamically on a web page. It uses Tree and CharMatrix classes to represent the underlying objects. Trees are displayed using "jstree" throughout this website, and <a href="run_mp.php">this page</a> provides an interface for executing exhaustive search in JavaScript.</p>
