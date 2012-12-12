/*
 * tree.js
 *
 * JavaScript library for implementing and manipulating trees.
 */

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
	leaves = taxa.map(leaf);
	while(leaves.length > 1) {
		var left = leaves.shift();
		var right = leaves.shift();
		leaves.push(node(left, right));
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
			var $upper = $("<div>").addClass('jstree-terminal-upper').addClass('jstree-upper');
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

$.fn.tree = function(tree) {
	makeTree(this, tree);
	return this;
}

$(function() {
	$(".jstree-tree").each(function() {
		var $tree = $(this);
		var treeWidth = parseInt($tree.css('width'), 10); 
		var $columns = $tree.find(".jstree-column");
		var depth = $columns.size();
		$columns.css({
			"min-width": (100 / depth) + '%'
		});
	});
});


