def param_to_query(params):
    if params is None or len(params) == 0:
        return ''
    query = '&'.join(k + '=' + v for k,v in params.items())
    return '?' + query

def uri(url, params):
    return url + param_to_query(params)
