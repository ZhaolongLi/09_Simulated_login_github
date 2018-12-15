# coding:utf-8

import requests
from lxml import etree

class Login(object):
    def __init__(self):
        self.headers = {
            'Referer':'https://github.com/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'Host':'github.com',
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()

    def get_token(self):
        """
        提取出authenticity_token
        :return:
        """
        response = self.session.get(self.login_url,headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div/form/input[2]/@value')[0]
        # try:
        #     token = token[0]
        #     return token
        # except:
        #     return None
        print(token)
        return token

    def login(self,email,password):
        """
        登录
        :param email:
        :param password:
        :return:
        """
        post_data = {
            'commit':'Sign in',
            'utf8':'✓',
            'authenticity_token':self.get_token(),
            'login':email,
            'password':password
        }
        response = self.session.post(self.post_url,data=post_data,headers=self.headers)
        if response.status_code == 200:
            self.dynamics_handle(response.text)

        response = self.session.get(self.logined_url,headers=self.headers)
        if response.status_code == 200:
            self.profile_handle(response.text)


    def dynamics_handle(self,html):
        """
        处理首页关注人的信息
        :param html:
        :return:
        """
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class,"news")]//div[contains(@class,"alert")]')
        for item in dynamics:
            dynamic =' '.join(item.xpath('.//div[@class="title"]//text()')).strip()
            print(dynamic)


    def profile_handle(self,html):
        """
        处理用户个人信息
        :param html:
        :return:
        """
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name,email)


if __name__ == '__main__':
    login = Login()
    login.login(email='',password='')

