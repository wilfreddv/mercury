def _iter_header(request):
    for line in request:
        yield line


def _get_post_data(data):
    if len(data):
        data = data.split('&')
        data_dict = {}
        for var in data:
            key, value = var.split('=')
            data_dict[key] = value

        return data_dict


def parse_request(request):
    req_dict = {}

    header = request.split('\r\n')[:-2]
    data = request.split('\n')[-1]
    data = _get_post_data(data)

    iterator = _iter_header(header)

    try:
        line = next(iterator)
    except StopIteration:
        # Bad request
        return {'400': "Bad request"}

    method, route, *_ = line.split(' ')
    req_dict['method'] = method
    req_dict['route'] = route
    req_dict['data'] = data

    try:
        for line in iterator:
            key, value = line.split(': ')
            req_dict[key] = value
    except StopIteration:
        pass

    return req_dict
