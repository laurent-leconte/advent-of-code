open Core.Deque

type content = Empty | Id of int

type slot = {
  start: int;
  len: int;
  content: content;
}

type got = Full of slot list | Partial of slot list


let string_of_slot slot =
  match slot.content with
  | Empty -> String.make slot.len '.'
  | Id id -> String.make slot.len (Char.chr (id mod 10 + 48))

let parse_input str =
  let ints = Utils.explode str |> List.map int_of_string in
  let slots = create () in
  let rec aux next_id start = function
    | [] -> ()
    | [a] -> let new_slot = {start; len = a; content = Id next_id} in
             enqueue_back slots new_slot;
    | a::b:: rest -> 
      enqueue_back slots {start; len = a; content = Id next_id};
      enqueue_back slots {start = start + a; len = b; content = Empty};
      aux (next_id + 1) (start + a + b) rest; in
  aux 0 0 ints;
  slots

let take_n_from_back slots n =
  let rec aux acc n =
    if n = 0 then Full(List.rev acc)
    else match dequeue_back slots with
      | None -> Partial(List.rev acc)
      | Some slot -> match slot.content with
              | Empty -> aux acc n
              | Id _ -> if slot.len <= n then
                            aux (slot :: acc) (n - slot.len)
                          else
                            let new_slot = {slot with len = slot.len - n} in
                            enqueue_back slots new_slot;
                            aux (slot :: acc) 0 in
aux [] n

let fold slots =
  let rec aux acc =
    match dequeue_front slots with
    | None -> List.rev acc (* no more slots, done*)
    | Some slot -> 
      match slot.content with
      | Id id -> aux (id :: acc) (* found a slot with an id, add it to the list *)
      | Empty -> (* fill the empty slot from the back of the queue *)



let part1 _ = 
  let input = "2333133121414131402" in
  let slots = parse_input input in
  Printf.printf "%s\n" (slots |> to_list |> List.map string_of_slot |> String.concat "");
  "done"