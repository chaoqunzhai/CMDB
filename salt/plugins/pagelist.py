
def page(table_data):
    all_count = len(table_data)
    count, free = divmod(all_count, 10)
    if free: count += 1
    parge_list = []
    for i in range(1, count):
        temp = '<a href="/salt/hostlist?p=%s">%s</a></li>' %(i,i)
        parge_list.append(temp)
    page_str = "".join(parge_list)
    return page_str