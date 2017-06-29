from salt.plugins.Salt_api_base import SaltBase

class SaltRun(SaltBase):
    __NOW=['rm','reboot']
    __timout = 300
    __type_list=['local','local_async','wheel','runner']
    """
        : tgt：即为target，执行该命令的目标机器、字符串或列表。
        : fun：字符串或列表，执行的模块
        : arg：列表或者一个由列表组成的列表，对应模块的参数。
        : timeout：Minion返回的超时时间。
    """
    def __init__(self,url,user,password):
        super(SaltRun,self).__init__(url,user,password)
        self.saltpostbase = SaltBase(url,user,password)
        self.token = self.saltpostbase.token_id()

    def Run_runner(self,obj):

        '''
        :支持runner 
        :   查看客户端状态 -manage.status
        :   查看job缓存  -jobs.list_jobs
        :支持wheel
        :   查看key_list  -key.list_all

        :list_all_key
        :manage_status
        :obj={'client': 'runner','fun': 'manage.status'}
        :a=A.Run_runner(obj)
        :
        :param obj: 
        :return: 
        '''
        obj={'client':obj['client'],'fun':obj['fun'],'timeout':self.__timout,}
        key_list = self.saltpostbase.PostRequest(obj)
        if obj['client'] == 'runner' and obj['fun'] == 'jobs.list_jobs':

            return key_list['return']

        elif obj['client'] == 'runner' and obj['fun'] == 'manage.status':

            down,up = key_list['return'][0].get('down'),key_list['return'][0].get('up')

            return down,up

        elif obj['client'] == 'wheel' and obj['fun'] == 'key.list_all':
            minions,minion_pre = key_list['return'][0]['data']['return']['minions'],key_list['return'][0]['data']['return']['minions_pre']
            return minions,minion_pre
        else:
            raise None

    def hostrun(self,tgt,fun,arg=None,test=True):
        '''
        A.hostrun('*','cmd.run','pwd')
        A.hostrun('*','pillar.items')
        ：制定主机执行模块
        :param tgt: *  主机ID
        :param fun: salt模块
        :param arg: 模块参数
        :return: 
        '''
        obj = {'client':'local','tgt':tgt,'fun':fun,'arg':arg,'timeout':self.__timout,'test':test}


        if arg not in self.__NOW:
            key_list = self.saltpostbase.PostRequest(obj)

            return key_list['return'][0]
        else:
            return None
    def grouprun(self,tgt,fun,arg=None,test=True):
        """
        grouprun('single-group','pillar.items')  
        grouprun('single-group','cmd.run','pwd')
        ：分组执行salt模块
        :param tgt: 组名
        :param fun: 方法
        :param arg:  参数
        :return: 
        """
        obj = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup',
               'timeout': self.__timout, 'test': test}
        if arg not in self.__NOW:


            key_list = self.saltpostbase.PostRequest(obj)
            return key_list['return'][0]
        else:
            raise None

    def host_sls(self,type,tgt,arg,test=True):
        '''
        A.host_sls('local_async','*126','init.env_init',test=True)
        有个小问题没有处理，如何设置env=prod
        ：按id来执行salt 状态文件
        :param type: 支持local,和local_async 
        :param tgt: 
        :param arg: 
        :param test: 
        :return: 
        '''

        if type in self.__type_list:
            obj = {'client': type, 'tgt': tgt, 'fun':'state.sls','arg':arg,'env_var':'prod','timeout':self.__timout,'test':test}
            key_list = self.saltpostbase.PostRequest(obj)
            return key_list['return'][0]

    def group_sls(self,type,tgt,arg,nodegroup=None,test=True):

        """
        ：指定主机执行sls状态文件
        :param type: 类型 
        :param tgt: 组名 或者 主机id
        :param arg: state.sls 参数  例如:init.env_init
        :param test: 测试
        A.group_sls('local','single-group','init.env_init', nodegroup=True,test=True)
        A.group_sls('local','*126','init.env_init',test=True)
        :return: 
        """
        if type in self.__type_list:
            if nodegroup:
                obj = {'client': type, 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup','timeout':self.__timout,'test':test}
            else:
                obj = {'client': type, 'tgt': tgt, 'fun': 'state.sls', 'arg': arg,
                       'timeout': self.__timout, 'test': test}
            key_list = self.saltpostbase.PostRequest(obj)

            return key_list['return'][0]
        else:return 'Not is type'
    def accept_key(self,type,minion_id):
        """
        : accept_key('wheel','single126')
        :param minion_id: 
        :return: 
        """
        if type in self.__type_list and type == 'wheel':
            obj = {'client':'wheel','fun':'key.accept','match':minion_id}
            key_list = self.saltpostbase.PostRequest(obj)
            return key_list['return'][0]

    def del_key(self,type,minion_id,):
        """
        
        :param type:  类型
        :param minion_id:  minion id
        :return: 
        """
        if type in self.__type_list and type == 'wheel':
            if minion_id != '*':
                obj = {'client':'wheel','fun':'key.delete','match':minion_id}
                key_list = self.saltpostbase.PostRequest(obj)
                return key_list['return'][0]

    def job_jib_status(self,type,jid):
        """
        :A.job_jib_status('wheel','20170629143854054866')
        :param type: 
        :param jid: 
        :return: 
        """
        if type in self.__type_list and type == 'runner':
            obj = {'client':'runner','fun':'jobs.lookup_jid','jid':jid}
            key_list = self.saltpostbase.PostRequest(obj)
            return key_list['return'][0]
        else:return 'not is client'

    def sync(self,type,minion_id,fun):
        """
        
        :param type: 
        :param fun:   sys.reload_modules and saltutil.sync_all 
        :param minion_id: 
        :return: 
        A.sync('local','*126','saltutil.sync_all')
        """
        __sync_all=['saltutil.sync_all','sys.reload_modules']
        if type in self.__type_list and type == 'local':
            if fun in __sync_all:
                obj = {'client': 'local', 'fun': fun, 'tgt': minion_id}
                key_list = self.saltpostbase.PostRequest(obj)
                return key_list['return'][0]



# A=SaltRun('https://172.16.30.133:7777','saltapi','saltapi')
# # A.minion('single125')
# # print(A)
# # obj={'client': 'local','fun': 'manage.status'}
# a=A.sync('local','*126','saltutil.sync_all')
#
# # a=A.host_sls('local_async','single127',)
# print('aaa',a)