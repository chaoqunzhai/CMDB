

def get_cookies(request):
    val = request.COOKIES.get('per_page_count')
    print('cookices',val,type(val))
    if val:
        val = int(val)
    else:
        val = int(10)
        return val
    return val