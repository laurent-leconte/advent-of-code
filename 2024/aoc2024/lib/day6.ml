type direction = Up | Down | Left | Right

module PointSet = Set.Make(struct
    type t = int*int
    let compare = compare
end)

let turn = function
  | Up -> Right
  | Right -> Down
  | Down -> Left
  | Left -> Up

let string_of_direction = function
  | Up -> "Up"
  | Down -> "Down"
  | Left -> "Left"
  | Right -> "Right"

let next_obstacle obstacles (x,y) direction =
    let add_distance = match direction with
      | Up -> (fun (a,b) -> if (a < x && b = y) then Some (x - a, a, b) else None)
      | Down -> (fun (a,b) -> if (a > x && b = y) then Some (a - x, a, b) else None)
      | Left -> (fun (a,b) -> if (a = x && b < y) then Some (y - b, a, b) else None)
      | Right -> (fun (a,b) -> if (a = x && b > y) then Some (b - y, a, b) else None) in
    obstacles
    |> List.filter_map add_distance
    |> List.sort (fun (a,_,_) (b,_,_) -> compare a b)
    |> Utils.head_opt    

let parse_input file =
    let map, m, n = Utils.read_char_matrix file in
    let obstacle_list = ref [] in
    let start = ref (0,0) in
    (* i, j -> ligne i, colonne j *)
    let walk_map i j c =
        if c.(i).(j) = '#' then obstacle_list := (i,j) :: !obstacle_list 
        else if c.(i).(j) = '^' then start := (i,j) in
    Utils.iterij walk_map map;
    (!start, !obstacle_list, map, m, n)

let before (a,b) = function
    | Up -> (a+1,b)
    | Down -> (a-1,b)
    | Left -> (a,b+1)
    | Right -> (a,b-1)

let find_edge (m,n) (x,y) = function
    | Up -> (0,y)
    | Down -> (m-1,y)
    | Left -> (x,0)
    | Right -> (x,n-1)

let trace_path obstacles (m,n) start =
    let rec aux acc (x,y) direction =
      match next_obstacle obstacles (x,y) direction with
      | None -> let end_point = find_edge (m,n) (x,y) direction in
                (end_point, direction)::acc
      | Some (_, a, b) -> 
          let new_point = before (a,b) direction in
          let new_direction = turn direction in
          aux ((new_point, new_direction)::acc) new_point new_direction in
    List.rev (aux [(start, Up)] start Up)

let make_segment (a,b) (c,d) = function
    | Up -> List.init (a - c + 1) (fun i -> (a-i,b))
    | Down -> List.init (c - a + 1) (fun i -> (a+i,b))
    | Left -> List.init (b - d + 1) (fun i -> (a,b-i))
    | Right -> List.init (d - b + 1) (fun i -> (a,b+i))

let rec visited seen_so_far = function
    | [] | [_] -> seen_so_far
    | ((a,b),dir)::(((c,d),_)::_ as tl) -> 
      let segments = make_segment (a,b) (c,d) dir in
      Printf.printf "Segments: %s\n" (String.concat "," (List.map (fun (x,y) -> Printf.sprintf "(%d,%d)" x y) segments));
      let add_to_set set (x,y) = PointSet.add (x,y) set in
      visited (List.fold_left add_to_set seen_so_far segments) tl

let part1 input =
    let start, obstacles, _, m, n = parse_input input in
    Printf.printf "Start: %d,%d\n" (fst start) (snd start);
    Printf.printf "Obstacles: %s\n" (String.concat "," (List.map (fun (x,y) -> Printf.sprintf "(%d,%d)" x y) obstacles));
    let path = trace_path obstacles (m,n) start in
    Printf.printf "Path: %s\n" (String.concat "," (List.map (fun ((x,y),dir) -> Printf.sprintf "(%d,%d) %s" x y (string_of_direction dir)) path));
    PointSet.cardinal (visited PointSet.empty path) |> string_of_int
