open Core.Deque

type slot = Empty | Id of int

type empty_slot = { len: int }
type file_slot = { len: int; id: int }

type slotv2 = EmptySlot of empty_slot | FileSlot of file_slot

let string_of_slot = function
  | Empty -> "."
  | Id id -> string_of_int id

let string_of_slotv2 = function
  | EmptySlot e -> String.make e.len '.'
  | FileSlot f -> String.make f.len (Char.chr (f.id + 48))

let str_of_slot_l l = l |> List.map string_of_slotv2 |> String.concat "|"

let parse_input str =
  let ints = Utils.explode str |> List.map int_of_string in
  let slots = create () in
  let add_to_back slot n = 
    for _ = 1 to n do
      enqueue_back slots slot
    done in
  let rec aux next_id = function
    | [] -> ()
    | [a] -> let new_slot = Id next_id in
             add_to_back new_slot a;
    | a::b:: rest -> 
      add_to_back (Id next_id) a;
      add_to_back Empty b;
      aux (next_id + 1) rest; in
  aux 0 ints;
  slots

let parse_input_v2 str =
  let ints = Utils.explode str |> List.map int_of_string in
  let rec aux next_id acc = function
    | [] -> List.rev acc
    | [a] -> let new_slot = FileSlot {len = a; id = next_id} in
             List.rev (new_slot :: acc)
    | a::b:: rest -> 
      let file = FileSlot {len = a; id = next_id} in
      let empty = EmptySlot {len = b} in
      let new_acc = if a > 0 then file :: acc else acc in
      let new_acc = if b > 0 then empty :: new_acc else new_acc in
      aux (next_id + 1) new_acc rest in
  aux 0 [] ints

let rec get_last_non_empty slots =
    match dequeue_back slots with
    | None -> None
    | Some slot -> 
      (match slot with
      | Id id -> Some id
      | Empty -> get_last_non_empty slots)

let fold slots =
  let rec aux acc =
    match dequeue_front slots with
    | None -> List.rev acc (* no more slots, done*)
    | Some slot -> 
      (match slot with
      | Id id -> aux (id :: acc) (* found a slot with an id, add it to the list *)
      | Empty -> (* fill the empty slot from the back of the queue *)
        (match get_last_non_empty slots with
        | None -> List.rev acc (* no more slots, done *)
        | Some id -> aux (id :: acc))) (* add the last slot to the results *)
    in 
  aux []

let check_sum list =
  let rec aux acc idx = function
    | [] -> acc
    | hd::tl -> 
      aux (acc + hd * idx) (idx + 1) tl in
  aux 0 0 list
  
let part1 input_file = 
  input_file
  |> Utils.read_lines
  |> List.hd
  |> parse_input
  |> fold 
  |> check_sum |> string_of_int
  (* Printf.sprintf "%s\n" (result |> List.map string_of_int |> String.concat "")*)

let find_appropriate_file len slots =
  (* let fuse n rest acc = 
    Printf.printf "Fusing %s with %s\n" (str_of_slot_l acc) (str_of_slot_l rest);
    match rest, acc with
    | EmptySlot e :: rest, EmptySlot e' :: rest' -> (List.rev rest)  @ (EmptySlot {len = e.len + e'.len + n} :: rest')
    | EmptySlot e :: rest, _ -> (List.rev rest)  @ (EmptySlot {len = e.len + n} :: acc)
    | _, EmptySlot e' :: rest' -> (List.rev rest)  @ (EmptySlot {len = e'.len + n} :: rest')
    | _ -> (List.rev rest) @ (EmptySlot {len = n} :: acc) in *)
  let rec aux seen = function
    | [] -> (None, [], seen)
    | EmptySlot e :: rest -> aux (EmptySlot e ::seen) rest
    | FileSlot f :: rest -> if f.len > len then 
         aux (FileSlot f :: seen) rest else (Some f, List.rev rest, seen) in
  let (file_opt, remaining, seen) = aux [] slots in
  (* Printf.printf "Looking for first file of len <= %d in %s\n" len (str_of_slot_l slots); *)
  (* Printf.printf "Found file %s, returning slots %s\n" (match file_opt with None -> "None" | Some f -> string_of_slotv2 (FileSlot f)) (str_of_slot_l remaining); *)
  (file_opt, remaining, seen)

let foldv2 slots =
  let append_fuse e = function
    | [] -> [EmptySlot e]
    | (FileSlot f :: rest) -> (EmptySlot e :: FileSlot f :: rest)
    | (EmptySlot e' :: rest) -> (EmptySlot {len = e.len + e'.len} :: rest) in
  let rec aux folded seen = function
    | [] -> (List.rev folded) @ seen
    | FileSlot f :: to_fold -> 
        Printf.printf "Moving file slot %s to the folded list\n" (string_of_slotv2 (FileSlot f));
        aux (FileSlot f :: folded) seen to_fold (* found a file, add it to the result *)
    | EmptySlot e :: to_fold ->  Printf.printf "Filling empty slot of size %d from %s\n" e.len (str_of_slot_l to_fold);
                                 Printf.printf "HAve already seen %s\n" (str_of_slot_l seen);
                              let file_opt, remaining_to_fold, new_seen = find_appropriate_file e.len (List.rev to_fold) in
                              Printf.printf "Found file %s. Remaining slots to fold after scan: %s. New files seen:%s\n" 
                                (match file_opt with None -> "None" | Some f -> string_of_slotv2 (FileSlot f)) 
                                (str_of_slot_l remaining_to_fold)
                                (str_of_slot_l new_seen);
                             (match file_opt with
                             | None -> (* no file small enough: all the files have been seen, finish *) 
                              aux (EmptySlot e :: folded) (new_seen @ seen) remaining_to_fold
                             | Some file -> 
                              if file.len = e.len then 
                                (* add the file, remove the empty slot, continue *)
                                aux (FileSlot file :: folded) (new_seen @ seen) remaining_to_fold 
                              else 
                                (* add the file, keep an empty slot, continue *)
                                let new_empty = {len = e.len - file.len} in
                              aux (FileSlot file :: folded) (new_seen @ seen) (append_fuse new_empty remaining_to_fold)) in
  aux [] [] slots

let part2 _ =
  let slots = parse_input_v2 "2333133121414131402" in
  print_endline (slots |> List.map string_of_slotv2 |> String.concat "|");
  print_endline "Starting fold";
  print_endline (slots |> foldv2 |> List.map string_of_slotv2 |> String.concat "|");
  "done"