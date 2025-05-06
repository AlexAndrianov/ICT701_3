_id_counter = 1

def next_id() -> int:
    global _id_counter

    id = _id_counter
    _id_counter += 1
    return id