(* Because programming is so much more fun in OCaml *)
type 'a tree =
	Leaf of 'a
	| Node of 'a tree * 'a tree
;;

let rec len t = match t with
	| Leaf _ -> 1
	| Node(l, r) -> len l + len r
;;

module IntSet = Set.Make( 
  struct
    let compare = Pervasives.compare
    type t = int
  end)

let rec fitch t f = match t with
	| Leaf i -> IntSet.singleton (f i), 0
	| Node(l, r) ->
		let l_set, l_len = fitch l f and
			r_set, r_len = fitch r f in
		let inter = IntSet.inter l_set r_set in
		if IntSet.is_empty inter then
			IntSet.union l_set r_set, l_len + r_len + 1
		else
			inter, l_len + r_len
;;

let all_trees_left l right = List.map (fun elt -> Node(elt, right)) l;;
let all_trees_right l left = List.map (fun elt -> Node(left, elt)) l;;

let rec trees_adding t taxon = match t with
	| Leaf l -> [Node(Leaf l, Leaf taxon)]
	| Node(l, r) -> Node(Leaf taxon, t)::((all_trees_left (trees_adding l taxon) r) @ (all_trees_right (trees_adding r taxon) l))
;;

let rec all_trees taxa = match taxa with
	| [] -> failwith "impossible"
	| t::[] -> [Leaf t]
	| hd::tl -> List.flatten(List.map (fun t -> trees_adding t hd) (all_trees tl))
;;
