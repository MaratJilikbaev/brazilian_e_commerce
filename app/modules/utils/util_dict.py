"""
See https://stackoverflow.com/questions/27265939/comparing-python-dictionaries-and-nested-dictionaries
"""


def diff_dict(d1, d2):
    """
    Compare two dicts and detect differences
    @return delta
    """

    def parse_deltas(deltas: dict):
        res = {}
        for k, v in deltas.items():
            if isinstance(v[0], dict):
                tmp = diff_dict(v[0], v[1])
                if tmp:
                    res[k] = tmp
            else:
                res[k] = v[1]

        return res

    def has_diff(d1, d2, o, tolerance=1e-6):
        v1, v2 = d1[o], d2[o]

        if isinstance(v1, float) and isinstance(v2, float):
            abs_diff = abs(v1 - v2)
            has_diff_above_tolerance = abs_diff > tolerance
            return has_diff_above_tolerance

        return v1 != v2

    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    shared_deltas = {o: (d1[o], d2[o]) for o in shared_keys if has_diff(d1, d2, o)}
    added_keys = d2_keys - d1_keys
    added_deltas = {o: (None, d2[o]) for o in added_keys}
    deltas = {**shared_deltas, **added_deltas}

    return parse_deltas(deltas)

