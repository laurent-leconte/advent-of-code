type instruction = Mul of int * int | Do | Dont
type state = Eval | Skip

let string_of_instruction = function
  | Mul (x, y) -> Printf.sprintf "Mul(%d, %d)" x y
  | Do -> "Do"
  | Dont -> "Dont"

let parse_instruction str =
  match str with
  | s when Str.string_match (Str.regexp "mul(\\([0-9]+\\),\\([0-9]+\\))") s 0 ->
      let x = int_of_string (Str.matched_group 1 s) in
      let y = int_of_string (Str.matched_group 2 s) in
      Mul (x, y)
  | "do()" -> Do
  | "don't()" -> Dont
  | _ -> failwith "Invalid instruction"

let parse_line str =
  let pattern = Str.regexp "\\(mul([0-9]++,[0-9]++)\\|do()\\|don't()\\)" in
  let rec aux pos acc =
    try
      let _ = Str.search_forward pattern str pos in
      let match_str = Str.matched_string str in
      let match_end_pos = Str.match_end () in
      let instruction = parse_instruction match_str in
      aux match_end_pos (instruction :: acc)
    with Not_found -> List.rev acc
  in
  let res = aux 0 [] in
  res

let eval_part1 instructions =
  let rec loop acc = function
    | [] -> acc
    | Mul (x, y)::tl -> loop (acc + x * y) tl
    | _::tl -> loop acc tl in
  loop 0 instructions

let eval_part2 instructions =
  let rec loop acc state = function
    | [] -> acc
    | Mul (x, y)::tl -> let new_acc = if state = Eval then acc + x * y else acc in
    loop new_acc state tl
    | Do::tl -> loop acc Eval tl 
    | Dont::tl -> loop acc Skip tl in
  loop 0 Eval instructions


let parse input = 
  input 
  |> Utils.read_lines 
  |> List.map parse_line
  |> List.concat

  let part1 input =
  input
  |> parse
  |> eval_part1
  |> string_of_int

  let part2 input =
    input
    |> parse
    |> eval_part2
    |> string_of_int