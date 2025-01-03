(** data loading **)

let read_lines name =
    let ic = open_in name in
    let try_read () =
        try Some (input_line ic) with End_of_file -> None in
    let rec loop acc = match try_read () with
        | Some s -> loop (s :: acc)
        | None -> close_in ic; List.rev acc in
    loop []

(** string manipulation **)

(* split according to a given separator *)
let split_by_string sep = Str.split (Str.regexp sep) 

let char_at s i = String.sub s i 1

(* transform a string into a list of chars *)
let explode s = List.init (String.length s) (char_at s) 

let explode_to_chars s = List.init (String.length s) (String.get s)

(** list helper functions **)

let rec transpose = function
   | [] 
   | [] :: _ -> []
   | rows    -> 
       List.map List.hd rows :: transpose (List.map List.tl rows)

(* returns a range from a to b inclusive *)
let range a b = 
    let start = min a b in
    let stop = max a b in
    List.init (stop - start + 1) (fun x -> start + x)

let sum = List.fold_left (+) 0

let take n l = 
    let rec loop hd tl = function
        | 0 -> (List.rev hd, tl)
        | n -> loop ((List.hd tl)::hd) (List.tl tl) (n-1) in
    loop [] l n

let bundle n l =
    let rec aux acc current j = function
        | [] -> List.rev ((List.rev current)::acc)
        | hd::tl as l -> if j = 0 then 
                            aux (List.rev current::acc) [] n l 
                         else 
                            aux acc (hd::current) (j-1) tl in
    aux [] [] n l

let fold f = function
  | [] | [_] -> failwith "Not enough items to fold list"
  | hd::tl -> List.fold_left f hd tl

let head_opt = function
    | [] -> None
    | hd::_ -> Some hd

(** matrix helper functions **)
let dim m =
    (Array.length m, Array.length m.(0))

let iterij f mat =
    let (m, n) = dim mat in
    for i = 0 to (m-1) do
        for j = 0 to (n-1) do
            f i j mat
        done
    done

(* Array doesn't have a foldi method, so implementing one ourselves *)
let foldi f x arr =
  let r = ref x in
  for i = 0 to (Array.length arr - 1) do
    r := f i !r arr.(i)
  done;
  !r

(* foldij for matrices *)
let foldij f =
    let fold_row i x arr =
        let g = f i in 
        foldi g x arr in
    foldi fold_row

let read_matrix file =
    let data = read_lines file in
    let n = List.length data in
    let m = String.length @@ List.hd data in
    let ground = Array.make_matrix n m 0 in
    let write_line i s =
        let line = List.map int_of_string (explode s) in
        let write_one j d = ground.(i).(j) <- d in
        List.iteri write_one line in
    List.iteri write_line data;
    (ground, n, m)

let read_char_matrix file =
    let data = read_lines file in
    let n = List.length data in
    let m = String.length @@ List.hd data in
    let ground = Array.make_matrix n m ' ' in
    let write_line i s =
        let line = explode_to_chars s in
        let write_one j d = ground.(i).(j) <- d in
        List.iteri write_one line in
    List.iteri write_line data;
    (ground, n, m)

let pad matrix pad_char pad_size =
    let (n, m) = dim matrix in
    let new_n = n + 2 * pad_size in
    let new_m = m + 2 * pad_size in
    let new_matrix = Array.make_matrix new_n new_m pad_char in
    let write_one i j d = new_matrix.(i + pad_size).(j + pad_size) <- d in
    iterij write_one matrix;
    new_matrix

(** memoize a recursive function **)
let memo_rec f =
  let h = Hashtbl.create 16 in
  let rec g x =
    try Hashtbl.find h x
    with Not_found ->
      let y = f g x in
      Hashtbl.add h x y;
      y
  in
  g

(** Tuple maps **)

let map_tuple f (a, b) = (f a, f b)

let map_triple f (a, b, c) = (f a, f b, f c)

(** print functions **)

let acc_str to_string acc x = acc ^ (to_string x) ^ " "

let print_array to_string arr =
     let f = acc_str to_string in
     print_endline @@ Array.fold_left f "" arr

let print_int_array = print_array string_of_int

let print_matrix to_string mat =
    let _ = Array.map (print_array to_string) mat in ()

let print_int_matrix = print_matrix string_of_int

let string_of_point (x,y) = (string_of_int x) ^ "," ^ (string_of_int y)

let print_list str_of_a l = print_endline @@ "[" ^ (String.concat ";" (List.map str_of_a l)) ^ "]"

let print_int_list = print_list string_of_int