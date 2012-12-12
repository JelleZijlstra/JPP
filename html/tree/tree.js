/*
 * tree.js
 *
 * JavaScript library for implementing and manipulating trees.
 */

var jstree = (function($) {

	function shuffleArray(array) {
		// Fisher-Yates shuffle
		var len = array.length;
		for(var i = len - 1; i > 0; i--) {
			var j = Math.floor(Math.random() * (i + 1));
			var tmp = array[i];
			array[i] = array[j];
			array[j] = tmp;
		}
		return array;
	}

	function TreeError(description) {
		this.description = description;
	}

	function Tree(params) {
		var terminal = (typeof params.name !== 'undefined');
		if(terminal) {
			var name = params.name;
		} else {
			var left = params.left;
			if(typeof left === 'undefined') {
				throw new TreeError("No left child given for non-terminal");
			}
			var right = params.right;
			if(typeof right === 'undefined') {
				throw new TreeError("No right child given for non-terminal");
			}
		}

		this.isTerminal = function() {
			return terminal;
		}
		this.name = function() {
			if(!terminal) {
				throw new TreeError("Cannot provide name for non-terminal");
			}
			return name;
		}
		this.children = function() {
			if(terminal) {
				throw new TypeError("Cannot provide children for terminal node");
			}
			return [left, right];
		}
	}

	function leaf(name) {
		return new Tree({name: name});
	}

	function node(left, right) {
		return new Tree({left: left, right: right});
	}

	Tree.prototype.toString = function() {
		if(this.isTerminal()) {
			return this.name();
		} else {
			var children = this.children();
			return '(' + children[0].toString() + ',' + children[1].toString() + ')';
		}
	};

	Tree.oneTree = function(taxa) {
		leaves = shuffleArray(taxa.map(leaf));
		while(leaves.length > 1) {
			var left = leaves.shift();
			var right = leaves.shift();
			leaves.push(node(left, right));
			shuffleArray(leaves);
		}
		return leaves[0];
	};

	var makeTree = (function() {
		var LEFT_NONE = 0;
		var LEFT_UP = 1;
		var LEFT_DOWN = 2;

		function make(tree, leftBorder) {
			if(tree.isTerminal()) {
				var $label = $("<div>").addClass('jstree-terminal-label').text(tree.name());
				var $upper = $("<div>").addClass('jstree-terminal-upper');
				if(leftBorder == LEFT_UP) {
					$upper.addClass('jstree-left-border');
				}
				var $lower = $("<div>").addClass('jstree-terminal-lower');
				if(leftBorder == LEFT_DOWN) {
					$lower.addClass('jstree-left-border');
				}
				var $line = $("<div>").addClass('jstree-terminal-node').append($upper).append($lower);
				var $row = $("<div>").addClass('jstree-terminal-row').append($line).append($label);
				return ($("<div>").addClass('jstree-terminal-container').append($row));
			} else {
				var children = tree.children();
				var $leftCorner = $("<div>").addClass('jstree-left').addClass('jstree-upper');
				if(leftBorder == LEFT_UP) {
					$leftCorner.addClass('jstree-left-border');
				}
				var $leftChild = $("<div>").addClass('jstree-right').append(make(children[0], LEFT_DOWN));
				var $upper = $("<div>").addClass('jstree-row').append($leftCorner).append($leftChild);


				var $rightCorner = $("<div>").addClass('jstree-left');
				if(leftBorder == LEFT_DOWN) {
					$rightCorner.addClass('jstree-left-border');
				}
				var $rightChild = $("<div>").addClass('jstree-right').append(make(children[1], LEFT_UP));
				var $lower = $("<div>").addClass('jstree-row').append($rightCorner).append($rightChild);

				var $tree = $("<div>").addClass('jstree-tree').append($upper).append($lower);
				return $tree;
			}
		}

		return function($elt, tree) {
			var $tree = make(tree, LEFT_NONE);
			$elt.append($tree);
		}
	})();

	// jQuery plugin
	$.fn.tree = function(tree) {
		makeTree(this, tree);
		return this;
	}

	// public API
	return {
		leaf: leaf,
		node: node,
		Tree: Tree,
		TreeError: TreeError
	};
})(jQuery);