<h2>Introduction to Maximum Parsimony</h2>
<p>In essence, maximum parsimony (MP) relies on finding a tree describing the relationships among taxa (operational units) that requires the smallest number of character changes during evolution.</p>

<h2>A simple example</h2>
<p>For example, suppose we have four species—A, B, C, and D. They vary in two characters: A has red eyes while B, C, and D have blue eyes; and A and B have a blue nose while C and D have a red one. We arbitrarily select A as the outgroup (the first-branching taxon). That means there are three possible trees:</p>

<ol>
	<li>
		<div class="jstree-stub" data-tree="node(leaf('A'), node(leaf('B'), node(leaf('C'), leaf('D'))))" />
	</li>

	<li>
		<div class="jstree-stub" data-tree="node(leaf('A'), node(leaf('C'), node(leaf('B'), leaf('D'))))" />
	</li>

	<li>
		<div class="jstree-stub" data-tree="node(leaf('A'), node(leaf('D'), node(leaf('C'), leaf('B'))))" />
	</li>
</ol>

<p>The character matrix (the input to our program) would look like this:</p>

<pre>
4 2
A 00
B 10
C 11
D 11
</pre>

<p>When using maximum parsimony, we want to select the tree that requires the fewest changes in character states. For all three trees above, there is one change in character 1: from 0 in A to 1 in the branch (clade) formed by B, C, and D. However, for character 2, trees (2) and (3) require two changes in state: from state 0 in A, it changed to 1 independently in C and D, or it changed to 1 in the B-C-D clade, and then back to 0 in B only. In either case, there are two state changes. In tree (1), on the other hand, the character changes only once in the branch leading to C and D.</p>

<p>Summing over the two characters, tree (1) has a length of 2, while trees (2) and (3) have a length of 3. Therefore, (1) is the most parsimonious tree. We conclude that C and D shared a more recent common ancestor with each other than either did with B.</p>

<h2>MP on larger datasets</h2>
<p>Real-world datasets tend to have more than four taxa and two characters. This poses a problem, because the number of possible trees increases very fast with the number of taxa—at O(n!). Therefore, it is impossible in practice to  enumerate all possible trees when there are more than ~10 taxa.</p>

<p>However, there are alternatives. These algorithms rely on the observation that optimal and near-optimal trees tend to be similar to each other. This is often visualized as a "tree landscape", where similar good trees are clustered together in "mountains". We then need a "hill-climbing" algorithm, which can move from a tree to other, similar trees in order to climb up the tree.</p>

<p>This is accomplished using heuristic algorithms that perform slight rearrangements on a tree in order to improve it—for example, exchange two adjacent nodes or branches of the tree. Common heuristic algorithms include:</p>
<ul>
	<li>Nearest Neighbor Interchange (NNI) – perform rearrangements of the type (A,(B,C)) -> (B,(A,C))</li>
	<li>Subtree Pruning Rebranching (SPR) – prune a random subtree from the tree, then replant that tree at a random different location in the tree.</li>
	<li>Tree Bissection Reconnection (TBR) – similar to SPR, but more powerful. The tree is bissected at a random node, and the two partial trees that result are both treated as unrooted and reconnected at random spots.</li>
</ul>

<p>Since these algorithms all rely on random rearrangements of a previous tree, they do not provide an exact solution. However, in practice they usually come at least close to finding the best tree when run for long enough.</p>
