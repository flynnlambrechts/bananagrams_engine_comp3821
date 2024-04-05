def add_tuple_elems(a: tuple, b: tuple) -> tuple:
    if len(a) != len(b):
        raise ValueError("Tuple lengths inconsistent")
    
    result = []
    for i in range(len(a)):
        result.append(a[i] + b[i])
        
    return tuple(result)