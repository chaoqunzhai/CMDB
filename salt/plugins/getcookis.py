

def get_cookies(request):
    val = request.COOKIES.get('per_page_count')
    val = int(val)
    return val