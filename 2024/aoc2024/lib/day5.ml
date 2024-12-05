module IntSet = Set.Make(Int)
module IntMap = Map.Make(Int)

type rule = Rule of int * int

type status = SeenFirst | SeenSecond | SeenNone

let parse_rule str =
  let pattern = Str.regexp "\\([0-9]+\\)|\\([0-9]+\\)" in
  let _ = Str.string_match pattern str 0 in
  let x = int_of_string (Str.matched_group 1 str) in
  let y = int_of_string (Str.matched_group 2 str) in
  Rule (x, y)

let parse_pages str =
  str |> String.split_on_char ',' |> List.map int_of_string

let parse input =
  let lines = input |> Utils.read_lines in
  let rec parse_rules acc = function
    | [] -> acc, []
    | hd::tl -> if hd = "" then acc, tl else parse_rules ((parse_rule hd)::acc) tl in
  let rules, remaining = parse_rules [] lines in
  let pages_list = List.map parse_pages remaining in
  rules, pages_list

let check_one_rule pages rule =
  let Rule (x, y) = rule in
  let rec aux seen_second = function
    | [] -> true
    | hd::tl -> if hd = x then not seen_second
                else if hd = y then aux true tl
                else aux false tl in
  aux false pages

let check_all_rules rules pages =
  List.for_all (check_one_rule pages) rules

let get_middle_element list =
  let n = List.length list in
  let middle = (n - 1) / 2 in
  List.nth list middle

let part1_compute (rules, pages_list) =
  Printf.printf "Before filtering: %d\n" (List.length pages_list);
  let filtered = List.filter (check_all_rules rules) pages_list in
  Printf.printf "After filtering: %d\n" (List.length filtered);
  let middle_elements = List.map get_middle_element filtered in
  Utils.sum middle_elements 

let part1 input = input |> parse |> part1_compute |> string_of_int

(* part 2 :
- build a DAG of the rules
- apply a topological sort to rank the numbers
- sort all pages according to the page rank
*)

let build_graph rules =
  (* Rule(x,y) means x < y, i.e. x is a predecessor of y *)
  let predecessors = IntMap.empty in
  let add_rule preds (Rule (x, y)) =
    preds
    (* add x to the graph if it isn't already in it *) 
    |> IntMap.update x (function
        | None -> Some IntSet.empty
        | Some set -> Some set) 
    (* add y to the predecessors of x *)
    |> IntMap.update y (function
        | None -> Some (IntSet.singleton x)
        | Some set -> Some (IntSet.add x set))  in
  List.fold_left add_rule predecessors rules

let print_graph graph =
  let print_set set =
    IntSet.iter (fun x -> Printf.printf "%d " x) set in
  IntMap.iter (fun k v -> Printf.printf "%d -> " k; print_set v; print_endline "") graph

let topological_sort graph =
  let find_no_predecessors graph =
    IntMap.bindings graph
    |> List.filter (fun (_, preds) -> preds = IntSet.empty)
    |> List.map fst in
  let update_graph graph to_remove =
    (* remove key from predecessors *)
    let graph = IntMap.remove to_remove graph in
    (* remove key from all its successors' predecessors *)
    let remove_key_from_set set = IntSet.remove to_remove set in
    IntMap.map remove_key_from_set graph in

  (* keep a list of nodes to visit, remove each node from the graph
  and update the list of nodes to visit *)
  let rec aux acc graph to_visit =
    match to_visit with
    | [] -> acc
    | hd::tl ->
      let new_graph = update_graph graph hd in
      let new_to_visit = find_no_predecessors new_graph in
      aux (hd::acc) new_graph (new_to_visit @ tl) in
  let ancestors = find_no_predecessors graph in
  print_endline (String.concat "," (List.map string_of_int ancestors));
  List.rev (aux [] graph ancestors)

let compare_from_list l x y =
  let rec aux = function
    | [] -> 0
    | hd::tl -> if hd = x then -1
                else if hd = y then 1
                else aux tl in
  aux l

let compare_from_rules rules x y =
  let rec aux = function
    | [] -> 0
    | Rule(a, b)::_ when a = x && b = y -> -1
    | Rule(a, b)::_ when a = y && b = x -> 1
    | _::tl -> aux tl in
  aux rules

let part2 input =
  let rules, pages_list = input |> parse in
  let passing, failing = List.partition (check_all_rules rules) pages_list in
  (* passing => part 1 *)
  let middle_elements = List.map get_middle_element passing in
  let part1_result = Utils.sum middle_elements in
  (* failing => part 2 *)
  let topological_compare = compare_from_rules rules in
  let sorted_failing = List.map (List.sort (topological_compare)) failing in
  let middle_elements = List.map get_middle_element sorted_failing in
  let part2_result = Utils.sum middle_elements in
  Printf.sprintf "%d %d" part1_result part2_result