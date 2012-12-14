<h2>Issues and areas for improvement</h2>
<p>I discussed performance in my <a href="design.php">discussion of design</a> and identified some areas where improvement seems possible. Here, I list these issues in a more condensed form, along with a few others:</p>
<ul>
	<li>The <tt>list_tree</tt> does not perform the length operation very efficiently. Introducing some form of intelligent caching might improve the performance of SPR and TBR.</li>
	<li>I should explore other strategies for parallelization (e.g., communicating only when a better tree has been found) and varying what data is communicated (e.g., include tree length in communication, so the master does not have to recalculate it). In general, the performance of parallel search currently seems anemic. With heuristic algorithms that can be run for any amount of time and make non-linear progress, it is impossible to calculate speedup in a conventional way, but it is clear that a 4-process parallel run of the program performs only marginally better than a serial version run for the same amount of time.</li>
	<li>On my computer, Python sometimes segfaults when run under MPI with less than four processes, with the stack trace indicating that the error occurs in libmpi. I have no idea what exactly causes this error.</li>
</ul>
