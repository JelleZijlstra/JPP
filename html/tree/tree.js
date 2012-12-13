/*
 * tree.js
 *
 * JavaScript library for implementing and manipulating trees.
 */

var jstree = (function($) {

	/*
	 * Randomly shuffle an array.
	 */
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

	/*
	 * Get the keys of an array.
	 */
	function getKeys(array) {
		return array.map(function(value, key) {
			return key;
		});
	}

	/*
	 * Set implementation, optimized for small integers
	 */
	function Set() {
		var length = arguments.length;
		var set = [];
		for(var i = 0; i < length; i++) {
			set[arguments[i]] = true;
		}
		this.contains = function(elt) {
			return set[elt] === true;
		};
		this.add = function(elt) {
			if(set[elt] !== true) {
				set[elt] = true;
				length++;
			}
		};
		this.remove = function(elt) {
			if(selt[elt] === true) {
				set[elt] = undefined;
				length--;
			}
		};
		this.size = function() {
			return length;
		};
		this.members = function() {
			return set.map(function(value, key) {
				return (value === true) ? key : undefined;
			}).filter(function(value) {
				return value !== undefined;
			});
		}
		this.intersection = function(otherSet) {
			var outSet = new Set();
			this.members().forEach(function(value) {
				if(otherSet.contains(value)) {
					outSet.add(value);
				}
			});
			return outSet;
		};
		this.union = function(otherSet) {
			var outSet = new Set();
			var adder = function(value) {
				outSet.add(value);
			}
			this.members().forEach(adder);
			otherSet.members().forEach(adder);
			return outSet;
		}
	}

	/*
	 * Constructor for custom exception class.
	 */
	function TreeError(description) {
		this.description = description;
	}

	/*
	 * Tree constructor.
	 */
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
		// Optional node label
		var label = params.label;
		var lengthCache = null;

		this.isTerminal = function() {
			return terminal;
		};
		this.name = function() {
			if(!terminal) {
				throw new TreeError("Cannot provide name for non-terminal");
			}
			return name;
		};
		this.children = function() {
			if(terminal) {
				throw new TypeError("Cannot provide children for terminal node");
			}
			return [left, right];
		};
		this.label = function() {
			return label;			
		};
		this.fitchLength = function(cm) {
			if(lengthCache === null) {
				var length = [];
				var nchars = cm.nchars();
				if(terminal) {
					for(var i = 0; i < nchars; i++) {
						length[i] = [new Set(cm.getTrait(name, i)), 0];
					}
				} else {
					var l = left.fitchLength(cm);
					var r = right.fitchLength(cm);
					for(var i = 0; i < nchars; i++) {
						var l_set = l[i][0];
						var r_set = r[i][0];
						var inter = l_set.intersection(r_set);
						if(inter.size() === 0) {
							length[i] = [l_set.union(r_set), l[i][1] + r[i][1] + 1];
						} else {
							length[i] = [inter, l[i][1] + r[i][1]];
						}
					}
				}
				lengthCache = length;
			}
			return lengthCache;
		};
	}

	/*
	 * Utility constructor functions.
	 */
	function leaf(name) {
		return new Tree({name: name});
	}

	function node(left, right) {
		return new Tree({left: left, right: right});
	}

	/*
	 * String conversion.
	 */
	Tree.prototype.toString = function() {
		if(this.isTerminal()) {
			return this.name();
		} else {
			var children = this.children();
			return '(' + children[0].toString() + ',' + children[1].toString() + ')';
		}
	};

	/*
	 * Tree length
	 */

	Tree.prototype.length = function(cm) {
		return this.fitchLength(cm).reduce(function(partial, data) {
			return partial + data[1];
		}, 0);
	};

	/*
	 * Build one random tree from taxa.
	 */
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

	/*
	 * Build an HTML representation of a tree.
	 */
	var makeTree = (function() {
		// codes for what cells to give a left border
		var LEFT_NONE = 0;
		var LEFT_UP = 1;
		var LEFT_DOWN = 2;

		function make(tree, leftBorder) {
			var label = tree.label();
			var hasLabel = typeof label !== 'undefined';
			if(tree.isTerminal()) {
				var $label = $("<div>").addClass('jstree-terminal-label').text(tree.name());
				var $upper = $("<div>").addClass('jstree-terminal-upper');
				if(leftBorder === LEFT_UP) {
					$upper.addClass('jstree-left-border');
				}
				if(hasLabel) {
					$content = $("<p>").addClass('jstree-branch-label').text(label);
					$upper.append($content);
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
				if(leftBorder === LEFT_UP) {
					$leftCorner.addClass('jstree-left-border');
				}
				if(hasLabel) {
					$content = $("<p>").addClass('jstree-branch-label').text(label);
					$leftCorner.append($content);
				}
				var $leftChild = $("<div>").addClass('jstree-right').append(make(children[0], LEFT_DOWN));
				var $upperHalf = $("<div>").addClass('jstree-row').append($leftCorner).append($leftChild);


				var $rightCorner = $("<div>").addClass('jstree-left');
				if(leftBorder === LEFT_DOWN) {
					$rightCorner.addClass('jstree-left-border');
				}
				var $rightChild = $("<div>").addClass('jstree-right').append(make(children[1], LEFT_UP));
				var $lowerHalf = $("<div>").addClass('jstree-row').append($rightCorner).append($rightChild);

				var $tree = $("<div>").addClass('jstree-tree').append($upperHalf).append($lowerHalf);
				return $tree;
			}
		}

		return function($elt, tree) {
			var $tree = make(tree, LEFT_NONE);
			$elt.append($tree);
		};
	})();

	/*
	 * Exhaustive search
	 */
	function treesAdding(tree, taxon) {
		if(tree.isTerminal()) {
			return [node(tree, taxon)];
		} else {
			var outTrees = [node(tree, taxon)];
			var children = tree.children();
			var leftTrees = treesAdding(children[0], taxon);
			for(var i = 0; i < leftTrees.length; i++) {
				outTrees.push(node(leftTrees[i], children[1]));
			}
			var rightTrees = treesAdding(children[1], taxon);
			for(var i = 0; i < rightTrees.length; i++) {
				outTrees.push(node(rightTrees[i], children[0]));
			}
			return outTrees;
		}
	}

	function allTreesRec(taxa) {
		if(taxa.length == 1) {
			return [leaf(taxa[0])];
		} else {
			var taxon = taxa.pop();
			var trees = [];
			var subTrees = allTreesRec(taxa);
			for(var i = 0, len = subTrees.length; i < len; i++) {
				trees = trees.concat(treesAdding(subTrees[i], leaf(taxon)));
			}
			return trees;
		}
	}

	function allTrees(taxa) {
		var outgroup = leaf(taxa.shift());
		var inTrees = allTreesRec(taxa);
		var outTrees = [];
		for(var i = 0, len = inTrees.length; i < len; i++) {
			outTrees.push(node(outgroup, inTrees[i]));
		}
		return outTrees;
	}

	function renameTerminals(tree, cm) {
		if(tree.isTerminal()) {
			return leaf(cm.getName(tree.name()));
		} else {
			var children = tree.children();
			return node(renameTerminals(children[0], cm), renameTerminals(children[1], cm));
		}
	}

	function exhaustiveSearch(cm) {
		var trees = allTrees(cm.taxonSet());
		var shortest = [];
		var length = null;
		for(var i = 0, len = trees.length; i < len; i++) {
			var treeLen = trees[i].length(cm);
			if(length === null || treeLen < length) {
				shortest = [trees[i]];
				length = treeLen;
			} else if(treeLen === length) {
				shortest.push(trees[i]);
			}
		}
		return [shortest.map(function(tree) {
			return renameTerminals(tree, cm);
		}), length];
	}

	/*
	 * Taxon-character matrix class
	 */
	function CharMatrix(matrix, taxa) {
		var ntaxa = taxa.length;
		var nchars = matrix[0].length;

		this.getName = function(id) {
			return taxa[id];
		};
		this.getTrait = function(taxon, char) {
			return matrix[taxon][char];
		};
		this.ntaxa = function() {
			return ntaxa;
		};
		this.nchars = function() {
			return nchars;
		};
		this.taxonSet = function() {
			return getKeys(taxa);
		};
	}
	CharMatrix.prototype.outgroup = function() {
		return this.getKeys()[0];
	};
	CharMatrix.prototype.ingroup = function() {
		return this.getKeys().slice(1);
	}
	CharMatrix.make = function(inputString) {
		var lines = inputString.split(/\n/);
		var intro = lines.shift();
		var splitLines = lines.map(function(line) {
			return line.split(/\s+/);
		});
		var taxa = splitLines.map(function(line) {
			return line[0];
		});
		var matrix = splitLines.map(function(line) {
			return line[1].split(/(?=.)/);
		});
		return new CharMatrix(matrix, taxa);
	};

	// jQuery plugin
	$.fn.tree = function(tree) {
		makeTree(this, tree);
		return this;
	};

	// automatically convert trees at load time
	$(function() {
		$('.jstree-stub').each(function() {
			var $location = $(this);
			/*
			 * eval is evil, but the alternative would be to write a parser for expressions like "(A,(B,C))".
			 * That's not impossible, and eventually it's what I'd like to do, but for now I'll keep it to this.
			 */
			var tree = eval($location.attr('data-tree'));
			$location.tree(tree);
		});
	});

	// public API
	return {
		leaf: leaf,
		node: node,
		Tree: Tree,
		TreeError: TreeError,
		allTrees: allTrees,
		CharMatrix: CharMatrix,
		exhaustiveSearch: exhaustiveSearch
	};
})(jQuery);
