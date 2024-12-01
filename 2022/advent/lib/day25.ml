let int_of_digit x =
  match x with
  | "0" -> 0
  | "1" -> 1
  | "2" -> 2
  | "-" -> -1
  | "=" -> -2
  | _ -> failwith @@ "Not a digit: " ^ x

let digit_of_int x =
  match x with
  | 0 -> "0"
  | 1 -> "1"
  | 2 -> "2"
  | 4 -> "-"
  | 3 -> "="
  | _ -> failwith @@ "Out of bound: " ^ (string_of_int x)


let int_of_number num =
  let rec aux pow acc = function
    | [] -> acc
    | x :: xs -> let d = int_of_digit x in
      aux (pow * 5) (acc + pow * d) xs 
  in
  num |> Utils.explode |> List.rev |> aux 1 0


let number_of_int i =
  print_endline @@ string_of_int i;
  let rec aux acc = function
    | 0 -> acc
    | x -> let d = x mod 5 in
      let num = digit_of_int d in
      let rem = if d < 3 then x / 5 else x / 5 + 1 in
      aux (num :: acc) rem
  in
  aux [] i |> String.concat ""

let part1 input =
  input
  |> Utils.read_lines
  |> List.map int_of_number
  |> List.fold_left (+) 0
  |> number_of_int
