module IntMap = Map.Make(Int)

let split_if_even_digits n =
  let s = string_of_int n in
  let len = String.length s in
  if len mod 2 = 0 then
    let half = len / 2 in
    let a = int_of_string (String.sub s 0 half) in
    let b = int_of_string (String.sub s half half) in
    Some (a, b)
  else
    None

let rec step l n =
  let do_one acc = function
    | 0 -> 1 :: acc
    | n -> (match split_if_even_digits n with
           | Some (a, b) -> b :: a :: acc
           | None -> n*2024 :: acc) in
  match n with
  | 0 -> l
  | n -> step (List.rev (List.fold_left do_one [] l)) (n-1)

let update_one_stone k v map =
  let update_list = function
    | 0 -> [1]
    | n -> (match split_if_even_digits n with
          | Some (a, b) -> [a; b]
          | None -> [n*2024]) in
    let new_k_list = update_list k in
    let add_to_map acc x = 
      let count = IntMap.find_opt x acc |> Option.value ~default:0 in
      IntMap.add x (count + v) acc in
    List.fold_left add_to_map map new_k_list

let rec part2 map = function
  | 0 -> map
  | n -> 
    let new_map = IntMap.fold update_one_stone map IntMap.empty in
    part2 new_map (n-1)
  
let map_of_list l =
  let add_to_map acc x = 
    IntMap.add x 1 acc in
  List.fold_left add_to_map IntMap.empty l

let sum_of_map map =
  IntMap.fold (fun _ v acc -> acc + v) map 0

let part1 _ = 
  let l = [554735;45401;8434;0;188;7487525;77;7] in
  let res = part2 (map_of_list l) 75 in
  string_of_int (sum_of_map res)