let parse_line str = 
  str |> String.split_on_char ' ' |> List.map int_of_string

let parse_input input = 
  input 
  |> Utils.read_lines 
  |> List.map parse_line

let differences l =
  let rec aux acc = function
    | [] -> acc
    | hd::tl -> match tl with
      | [] -> acc
      | hd2::_ -> aux ((hd2 - hd)::acc) tl in
  List.rev (aux [] l)

let all_positive l = List.for_all (fun x -> x > 0) l

let all_negative l = List.for_all (fun x -> x < 0) l

let monotonic l = all_positive l || all_negative l

let capped_increments l = List.for_all (fun x -> abs(x) <= 3) l

let safe_diff l = capped_increments l && monotonic l

let safe l = safe_diff (differences l)

let part1 input =
  let levels = parse_input input in
  let diffs = List.map differences levels in
  let safe_levels = List.filter safe_diff diffs in
  string_of_int (List.length safe_levels)


let sublists l = (* generate all sublists with n-1 elements *)
  let rec aux acc rev_head = function
    | [] -> acc
    | hd::tl -> let new_sublist = List.rev rev_head @ tl in
                let new_head = hd::rev_head in
                aux (new_sublist::acc) new_head tl in
  List.rev (aux [] [] l)

let conditionally_safe l =
  if safe l then true else
  let sublists = sublists l in
  List.exists safe sublists

let part2 input =
  let levels = parse_input input in
  let cond_safe_levels = List.filter conditionally_safe levels in
  string_of_int (List.length cond_safe_levels)