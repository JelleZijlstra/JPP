<script type="text/javascript">
	$(function() {
		$("#tree-cm-submit").click(function() {
			var cmStr = $("#tree-cm").val();
			try {
				var cm = jstree.CharMatrix.make(cmStr);
			} catch(e) {
				alert("Could not parse character matrix");
				return;
			}
			var trees = jstree.exhaustiveSearch(cm);
			$("#results").hide();
			$("#tree-length").text(trees[1]);
			var ntrees = trees[0].length;
			$("#tree-n").text(ntrees);
			var $loc = $("#tree-loc");
			for(var i = 0; i < ntrees; i++) {
				$loc.tree(trees[0][i]);
			}
			$("#results").show();
		});
	});
</script>
<style type="text/css">
	#tree-cm {
		height: 100px;
		width: 100%;
	}
</style>
<h2>Exhaustive maximum-parsimony tree search</h2>

<form class="input">
	<label for="cm">
		<p>Input your character matrix here in the form:</p>

<pre>
4 2
A 00
B 10
C 11
D 11
</pre>

		<p>The first line gives the number of taxa, then the number of characters. Taxon names cannot have whitespace in them.</p>

		<p>Do <strong>not</strong> run this script with more than ~9 taxa in the matrix&mdash;the time required for the computation rapidly passes the age of the universe.</p>
	</label>
	<textarea name="cm" id="tree-cm"></textarea>
	<input type="button" id="tree-cm-submit" value="Find best trees"></input>
</form>

<div id="results" style="display: none;">
	<h3>Results</h3>

	<p>Tree length: <span id="tree-length"></span>.</p>
	<p>Number of trees: <span id="tree-n"></span>.</p>

	<div id="tree-loc"/>
</div>
