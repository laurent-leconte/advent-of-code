let memo = Hashtbl.create 100

let concat a b =
  Z.of_string (Z.to_string a ^ Z.to_string b)

let rec generate_ops n =
  if Hashtbl.mem memo n then
    Hashtbl.find memo n
  else
    let result =
      if n = 0 then
        [[]]
      else
        let smaller_lists = generate_ops (n - 1) in
        List.concat [
          List.map (fun lst -> Z.add :: lst) smaller_lists;
          List.map (fun lst -> Z.mul :: lst) smaller_lists;
          List.map (fun lst -> concat :: lst) smaller_lists
        ]
    in
    Hashtbl.add memo n result;
    result

let rec test target nums ops =
  match (nums, ops) with
  | [], _ -> false
  | [a], _ -> Z.equal a target 
  | a::b::rest, op::ops -> let c = op a b in 
                           test target (c::rest) ops
  | _, _ -> false

let parse_line input =
  match Utils.split_by_string ": " input with
  | [target_str; nums_str] ->
      let target = Z.of_string target_str in
      let nums = List.map Z.of_string (String.split_on_char ' ' (String.trim nums_str)) in
      (target, nums)
  | _ -> failwith "Invalid input format"

let test_line (target, input) =
  let all_ops = generate_ops (List.length input - 1) in
  if List.exists (fun ops -> test target input ops) all_ops then target else Z.zero

let part1 input_file =
input_file 
|> Utils.read_lines 
|> List.map parse_line 
|> List.map test_line 
|> List.fold_left Z.add Z.zero
|> Z.to_string