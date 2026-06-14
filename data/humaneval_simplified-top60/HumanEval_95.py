from typing import Dict, Any


def check_dict_case(dict: Dict[Any, Any]) -> bool:
    if not dict:
        return False
    state = None
    for key in dict:
        if not isinstance(key, str):
            return False
        if state is None:
            state = "upper" if key.isupper() else "lower" if key.islower() else None
            if state is None:
                return False
        elif (state == "upper" and not key.isupper()) or (
            state == "lower" and not key.islower()
        ):
            return False
    return state in ("upper", "lower")
