
z= [{'role_type__name': '翟超群', 'role_type__salt_run__statues': 0, 'kernel': 'Centos7', 'disk': '1024G', 'ip': '192.168.22.100', 'source': 0, 'id': 1}, {'role_type__name': '翟超群', 'role_type__salt_run__statues': 0, 'kernel': 'Centos7', 'disk': '1024G', 'ip': '192.168.22.100', 'source': 0, 'id': 1}, {'role_type__name': 'zcq-2', 'role_type__salt_run__statues': 0, 'kernel': 'centos7', 'disk': '2024', 'ip': '192.168.22.1', 'source': 2, 'id': 2}, {'role_type__name': 'zcq-2', 'role_type__salt_run__statues': 0, 'kernel': 'centos7', 'disk': '2024', 'ip': '192.168.22.1', 'source': 2, 'id': 2}, {'role_type__name': 'zcq-2', 'role_type__salt_run__statues': 0, 'kernel': 'centos6.5', 'disk': '1024', 'ip': '192.168.1.200', 'source': 3, 'id': 3}, {'role_type__name': 'zcq-2', 'role_type__salt_run__statues': 0, 'kernel': 'centos6.5', 'disk': '1024', 'ip': '192.168.1.200', 'source': 3, 'id': 3}]
b=[]

for dic in [each.items() for each in z]:
    # print(dic)
    if dic in b:
        continue
    else:
        b.insert(0,dic)
print(b)
# func = lambda z:dict([(x, y) for y, x in z.items()])
# print(func(func(z)))
