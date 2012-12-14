<h2>Design and performance</h2>
<p>Here, I discuss the design and organization of the Python code of JPP. Overall, I tried to design the program in a modular way, where it is easy to swap components (e.g., heuristic algorithms) without affecting the rest of the program and to change the implementation of one component without affecting another. However, in some cases there is a tight connection between components that ideally should be separate (e.g., the SPR and TBR implementations directly manipulate list_tree objects).</p>

<h3>Representation of trees</h3>
<p>Trees are the central objects of any phylogenetics program, and it is important to decide how to represent them. Initially, I used recursive, immutable objects containing either the name of a terminal node or references to two child trees, an obvious, elegant approach (see <tt>tree.py</tt> for the implementation). One of the most expensive operations on trees is the calculation of tree length, and the fact that these trees are immutable and nested makes it easy to share subtrees among different tree objects and cache length calculations in those subtrees. This optimization improves the performance of exhaustive search on the <tt>data/data3.txt</tt> datafile by around 60% on my computer: running time goes down from 2.5 s to 1.0 s. This approach of immutable, nested objects worked well for exhaustive search, but I ran into problems while implementing heuristic search algorithms. TBR, for example, requires access to random nodes in the tree and a way to insert nodes in the middle of an existing tree. Furthermore, it requires that the tree is treated as unrooted, but the <tt>tree</tt> object imposes a natural ordered, rooted structure on the tree. Therefore, I implemented an alternative approach, the <tt>list_tree</tt>, which represents a tree as a list of nodes containing pointers (list indices) to adjacent nodes. This makes it feasible (if tricky, because different nodes need to be kept synchronized) to grab random nodes and to modify the tree in-place. However, the <tt>list_tree</tt> does not perform as well on some operations (i.e., tree length) as the <tt>tree</tt> does, since it does not cache length computations, and doing so would be tricky and error-prone because modifications to the tree would need to invalidate parts of the cache.</p>

<h3>Exact algorithms</h3>
<p>Exhaustive search is implemented by starting with the unique tree containing a single taxon, then recursively generating more trees by adding a taxon at all possible nodes. For example, on the tree</p>

<div class="jstree-stub" data-tree="node(leaf('A', 2), leaf('B', 3), 1)"/>

<p>we can add the taxon C on each of the locations 1, 2, and 3, generating the following three trees:</p>

<ol>
	<li>
		<div class="jstree-stub" data-tree="node(leaf('C'), node(leaf('A'), leaf('B')))"/>
	</li>
	<li>
		<div class="jstree-stub" data-tree="node(node(leaf('C'), leaf('A')), leaf('B'))"/>
	</li>
	<li>
		<div class="jstree-stub" data-tree="node(leaf('A'), node(leaf('C'), leaf('B')))"/>
	</li>
</ul>

<p>Two major optimizations help keep the performance of exhaustive search reasonable up to around 10 taxa: caching of length calculations (discussed above) and extensive use of generators, so that trees are created and examined one by one without keeping unneeded trees in memory, rather than building up an enormous list of trees and only then examining their length. When I replaced all generators with lists, performance became terrible: for 9 taxa, the program took 16 s and 11 MB of memory to calculate the best tree, but without generators, peak memory usage increased to 2.7 GB and the program ran for 11 minutes before I killed it.</p>

<p>Branch-and-bound search is similar to exhaustive search, but immediately discards partial trees whose length is greater than that of the best full tree. For 9 taxa, this brings running time down from 16 s to 5 s for the <tt>data/data4.txt</tt> datafile on my computer.</p>

<h3>Heuristic algorithms</h3>
<p>Among the three heuristic algorithms used, I implemented NNI to operate on <tt>tree</tt> objects and SPR and TBR to operate on <tt>list_tree</tt>s. NNI appears to perform rearrangements faster, probably because it can take advantage of caching in calculating tree length. However, NNI performs only local rearrangements on a tree, and therefore I suspect that it is less good than SPR and TBR at jumping from one promising hilltop to another. When I ran each algorithm for one minute in a single process on <tt>data/oryzos.txt</tt>, I obtained shortest trees of length 939 with NNI, 975 with SPR, and 1037 with TBR (less is better).</p>

<p>For all three heuristic algorithms, I implemented parallel search using a similar process: the different MPI processes each run a heuristic algorithm, and periodically communicate by sending the best trees found to the master process. The master compares the trees and performs tree fusion to unite the trees into a single ideal tree, then sends each process a tree to continue the search on. In the "mixed" algorithm, which appears to perform best in parallel, different processes run different algorithms.</p>

<p>Overall, the performance of the parallelization has been disappointing to me. I ran the program on the dataset in data/oryzos.txt, with a communication interval of 15 s, using TBR, under the following three configurations:</p>
<ul>
	<li>Single process, run for 2 min &ndash; produces a single tree of length 973</li>
	<li>Single process, run for 8 min &ndash; produces a single tree of length 918</li>
	<li>Four processes, run for 2 min &ndash; produce a single tree of length 961</li>
</ul>
<p>I also ran the program under the "mixed" configuration with four processes for two minutes with an interval of 15 s. This yielded a tree of length 934.</p>

<p>Thus, the multiple processes together perform better than a single process, but not nearly as well as a single process run longer. This suggests that the strategy used for communicating between the processes is not yet optimal. I have not hade time to explore other communication paradigms (for example, having processes communicate as soon as they find an improved tree, rather than at set intervals).</p>

