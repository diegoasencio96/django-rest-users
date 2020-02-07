from rest_framework.response import Response


def build_default_success_response(message, status, extra_data):
    data = {'detail': message}
    if extra_data:
        data.update(extra_data)
    return Response(data, status=status)


def get_ok_response(message, status=200, extra_data=None):
    builder = build_default_success_response
    return builder(message=message, status=status, extra_data=extra_data)


def get_bad_response(message, status=400, extra_data=None):
    builder = build_default_success_response
    return builder(message=message, status=status, extra_data=extra_data)

