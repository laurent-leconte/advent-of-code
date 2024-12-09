module CharMap = Map.Make(Char)

module PointSet = Set.Make(struct
    type t = int * int
    let compare = compare
  end)

let parse_input input_file =
  let mat, m, n = Utils.read_char_matrix input_file in
  let do_one i j map c =
    if c = '.' then
      map
    else
      match CharMap.find_opt c map with
      | None -> CharMap.add c [(i, j)] map
      | Some lst -> CharMap.add c ((i, j) :: lst) map in
  Utils.foldij do_one CharMap.empty mat, m, n


let add_antinodes_part1 set ((xa, ya), (xb, yb)) = 
  PointSet.add (2*xa - xb, 2*ya - yb) 
    (PointSet.add (2*xb - xa, 2*yb - ya) set)

let add_antinodes_part2 m n set ((xa, ya), (xb, yb)) = 
  let mn = max m n in
  let in_map (x, y) = x >= 0 && x < m && y >= 0 && y < n in
  let new_points = List.init (2*mn + 3) (fun i -> (xa + (i - mn - 1) * (xb - xa), ya + (i - mn * (yb - ya)))) in
  List.fold_left (fun acc p -> if in_map p then PointSet.add p acc else acc) set new_points
  (* first, change the points around to have positive deltas
  if (xa > xb) then add_antinodes_part2 m n set ((xb, yb), (xa, ya))
  else if xa = xb then
    (if ya > yb then add_antinodes_part2 m n set ((xb, yb), (xa, ya))
    else
    (* dy > 0 *)
      let dy = yb - ya in
      let y_min, y_max = -ya / dy, (n - ya)/dy + 1 in
      let new_points = List.init (y_max - y_min + 1) (fun i -> (xa, ya + i * dy))  in
      List.fold_left (fun acc p -> if in_map m n p then PointSet.add p acc else acc) set new_points)
  else
  (* dx > 0 *)
  let dx, dy = xb - xa, yb - ya in
  *)

let add_antinodes idx_list set ((xa, ya), (xb, yb)) = 
  let dx, dy = xb - xa, yb - ya in
  List.fold_left (fun acc i -> PointSet.add (xa + i * dx, ya + i * dy) acc) set idx_list

let combine_two list =
  let rec combine_two' acc = function
    | [] -> acc
    | x::xs -> combine_two' (List.map (fun y -> (x, y)) xs @ acc) xs in
  combine_two' [] list

let generic idx_list input_file =
  let map, m, n = parse_input input_file in
  let antinodes = CharMap.fold (fun _ lst acc -> 
    List.fold_left (add_antinodes idx_list) acc (combine_two lst)) map PointSet.empty in
  let in_map (x, y) = x >= 0 && x < m && y >= 0 && y < n in
  PointSet.filter in_map antinodes |>
  PointSet.cardinal |> string_of_int

let part1 input_file =
  generic [-1; 2] input_file
  (*
  let map, m, n = parse_input input_file in
  let antinodes = CharMap.fold (fun _ lst acc -> 
    List.fold_left add_antinodes_part1 acc (combine_two lst)) map PointSet.empty in
  let in_map (x, y) = x >= 0 && x < m && y >= 0 && y < n in
  PointSet.filter in_map antinodes |>
  PointSet.cardinal |> string_of_int *)

let part2 input_file =
  let idx_list = List.init 101 (fun i -> i - 50) in
  generic idx_list input_file
  