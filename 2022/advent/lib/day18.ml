let are_adjacent (x1, y1, z1) (x2, y2, z2) = abs (x1 - x2) + abs (y1 - y2) + abs (z1 - z2) = 1

let point_of_line s =
  match Utils.split_by_string "," s with
    | [x;y;z] -> (int_of_string x, int_of_string y, int_of_string z)
    | _ -> failwith "Bad format"

let acc_and_count (old, cnt) new_item =
  let is_adjacent = are_adjacent new_item in
  let count_adjacent = List.length (List.filter is_adjacent old) in
  (new_item::old, cnt + 6 - 2*count_adjacent)

let part1 input =
  Utils.read_lines input
  |> List.map point_of_line
  |> List.fold_left acc_and_count ([], 0)
  |> snd
  |> string_of_int

let both_parts input = (part1 input, "")