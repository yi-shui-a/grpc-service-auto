from global_var import response_dict

import copy


def getResponse(code: int, message: str) -> dict:
    res = copy.deepcopy(response_dict)
    res["code"] = code
    res["message"] = message
    return res
