def parse_tuple(tuple_string):
    tuple_string = tuple_string.strip()
    if tuple_string[0] != "(" or tuple_string[-1] != ")":
        raise ValueError(f"Not a valid tuple for this function -> {tuple_string}")
    tuple_str = tuple_string[1:-1] # Remove the brackets
    first_value, second_value = tuple_str.split(",", 1)
    return first_value.strip(), second_value.strip()

def parse_multiple_tuple_strings(tuple_strings):
    tuple_strings = tuple_strings.strip()
    if not tuple_strings:
        return []

    if tuple_strings[0] != "(" or tuple_strings[-1] != ")":
        raise ValueError(f"Not a valid tuple list for this function -> {tuple_strings}")

    tuple_strings = tuple_strings[1:-1]
    return [parse_tuple(f"({ts})") for ts in tuple_strings.split('),(')]

if __name__ == "__main__":
    print("Hi")