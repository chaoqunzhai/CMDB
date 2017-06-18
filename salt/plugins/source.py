from salt import models


class SourceBase(object):
    _i = None

    def __init__(self):
        self.source_type = models.Hostname.source_choirce
        self.source_type_dict = {}
        for i in self.source_type:
            self.source_type_dict[i[0]] = i[1]
        # print(self.source_tyope_dict)

    @classmethod
    def instance(cls):
        if cls._i:
            return cls._i
        else:
            cls._i =SourceBase()
            return cls._i
    @property
    def sorce_type(self):

        return self.source_type_dict
