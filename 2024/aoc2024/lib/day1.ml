module IntMap = Map.Make(Int)

let line_to_tuple line =
  let parts = Utils.split_by_string "   " line in
  let a = List.nth parts 0 |> int_of_string in
  let b = List.nth parts 1 |> int_of_string in
  (a, b)

let parse_input input = 
  input 
  |> Utils.read_lines 
  |> List.map line_to_tuple
  |> List.split

let part1 input =
let a_list, b_list = parse_input input in
let a_sorted = List.sort compare a_list in
let b_sorted = List.sort compare b_list in
let rec aux acc a b = match a, b with
  | [], [] -> acc
  | hd_a::tl_a, hd_b::tl_b -> aux (acc + abs(hd_a - hd_b)) tl_a tl_b
  | _, _ -> failwith "Lists have different lengths" in
string_of_int (aux 0 a_sorted b_sorted)


let counter list =
  let rec aux acc = function
    | [] -> acc
    | hd::tl -> aux (IntMap.update hd (function
      | None -> Some 1
      | Some x -> Some (x + 1)) acc) tl in
  aux IntMap.empty list

let part2 input =
  let a_list, b_list = parse_input input in
  let b_counter = counter b_list in
  let rec aux acc a = match a with
    | [] -> acc
    | hd::tl -> match IntMap.find_opt hd b_counter with
      | None -> aux acc tl
      | Some x -> aux (acc + hd * x) tl in
  string_of_int (aux 0 a_list)