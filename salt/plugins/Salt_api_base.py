import requests
import json

class SaltBase(object):
    __token_id = ''
    def __init__(self,url,user,passwrd):
        self.__url= url
        self.__user = user
        self.__password =passwrd

    def PostRequest(self,obj, prefix="/",*args,**kwargs):
        headers = {'X-Auth-Token': self.__token_id}
        if obj:

            url = self.__url + prefix
            req = requests.post(url=url,data=obj,headers=headers,verify=False)

        else:
            print(kwargs)
            url=self.__url + prefix
            print('posturl-',url)
            req = requests.post(url=url,headers=headers,verify=False)
            print(req.text,req.headers)

        return req.json()


    def token_id(self):
        obj = {'eauth': 'pam', 'username': self.__user,'password': self.__password}
        content = self.PostRequest(obj,prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
            print(self.__token_id)
        except KeyError:
                raise KeyError





