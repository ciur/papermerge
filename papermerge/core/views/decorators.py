import json
from django.http import (
    HttpResponse,
    HttpResponseRedirect
)


def smart_dump(value):

    if isinstance(value, str):
        return json.dumps({'msg': value})

    if isinstance(value, dict):
        return json.dumps(value)

    return ""


def json_response(func):
    """
    Decorates view to return application/json type response.
    Argument function func is expected to return one of:

        1. A string
            in this case, body will be a json.dump({
                'msg': returned_str
            })
            and status code will be 200
        2. A dictionary
            same as above, but respone will dump directly dictionary
                json.dumps(returned_dict)
            and status code will be 200
        3. Two valued tuple
            First value of the tuple must be either a string
            or a dictionary. In this case above points 1 and 2 apply
            Second value of the tuple is status code (as intiger number)
    """
    def inner(*args, **kwargs):
        ret = func(*args, **kwargs)
        status = 200
        body = ""

        if isinstance(ret, str) or isinstance(ret, dict):
            body = smart_dump(ret)
        elif isinstance(ret, tuple):
            for_body = ret[0]
            status = ret[1]
            body = smart_dump(for_body)
        elif isinstance(ret, HttpResponseRedirect):
            # in case anonymous user access this view - return
            # the HttpResponseRedirect object
            return ret
        else:
            raise ValueError(
                "Function must return str, dict or 2 valued tuple"
            )

        return HttpResponse(
            body,
            content_type="application/json",
            status=status
        )

    return inner

