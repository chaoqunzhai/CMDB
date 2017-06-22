class BaseServiceList(object):
    def __init__(self, condition_config, table_config):
        # 查询条件的配置，列表
        self.condition_config = condition_config

        # 表格的配置，列表
        """
        {
            'q': 'title',       # 用于数据库查询的字段，即Model.Tb.objects.xxx.values(*['v',]), None则表示不获取相应的数据库列
            'title': '标题',     # table表格显示的列名
            'display': 0        # 实现在表格中显示 0，不显示；1显示
            'text': {'content': "{id}", 'kwargs': {'id': '@id'}}, # 表格的每一个td中显示的内容,一个@表示获取数据库查询字段，两个@@，表示根据当前id在全局变量中找到id对应的内容
            'attr': {}          # 自定义属性
        }
        """
        self.table_config = table_config
