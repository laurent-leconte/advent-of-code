let rec check_string matrix list i j idir jdir =
  match list with
    | [] -> true
    | hd::tl -> 
      if i < 0 || j < 0 || i >= Array.length matrix || j >= Array.length matrix.(0) then false
      else if matrix.(i).(j) <> hd then false
      else check_string matrix tl (i+idir) (j+jdir) idir jdir


let check_part_2 matrix i j =
  let diag_ok char1 char2 = (char1 = 'S' && char2 = 'M') || (char1 = 'M' && char2 = 'S') in
  if matrix.(i).(j) <> 'A' then false
  else (diag_ok matrix.(i-1).(j-1) matrix.(i+1).(j+1)) && (diag_ok matrix.(i-1).(j+1) matrix.(i+1).(j-1))
      

let count_matches matrix str =
  let all_dirs = [(0, 1); (1, 0); (-1, 0); (0, -1); (1, 1); (1, -1); (-1, 1); (-1, -1)] in
  let (m, n) = Utils.dim matrix in
  let list = Utils.explode_to_chars str in
  let check_one_dir i j (idir, jdir) = if (check_string matrix list i j idir jdir) then 1 else 0 in
  let count = ref 0 in
  for i = 0 to m-1 do
    for j = 0 to n-1 do
      all_dirs |> List.map (check_one_dir i j) |> Utils.sum |> (fun x -> count := !count + x)
    done
  done;
  !count

let count_part2 matrix =
  let (m, n) = Utils.dim matrix in
  let count = ref 0 in
  for i = 1 to m-2 do
    for j = 1 to n-2 do
      if check_part_2 matrix i j then count := !count + 1
    done
  done;
  !count
  

let part1 input =
  let matrix, _, _ = Utils.read_char_matrix input in
  let str = "XMAS" in
  count_matches matrix str |> string_of_int

let part2 input =
  let matrix, _, _ = Utils.read_char_matrix input in
  count_part2 matrix |> string_of_int