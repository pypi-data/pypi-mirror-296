def zmap(
    v: float, low_in: float, high_in: float, low_out: float, high_out: float
) -> float:
    v = min(max(v, low_in), high_in)
    percent = (v - low_in) / (high_in - low_in)
    return percent * (high_out - low_out) + low_out


def bind_method(roots: list[int], methods: list[int], method_map: dict) -> list:
    ret: list = []
    for i in range(len(roots)):
        method = method_map.get(i % len(methods))
        if method is None:
            ret.append(None)
        elif not isinstance(method, list):
            ret.append(method + roots[i])
        else:
            ret.append([m + roots[i] for m in method])
    return ret
