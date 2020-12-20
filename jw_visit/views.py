# -*- coding=utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
# Create your views here.
import json
import random
from pprint import pprint

import requests
import time
from lxml import etree
from jw_visit.hex2b64 import HB64
import jw_visit.RSAJS
class Longin():
    def __init__(self,user,passwd,base_url, login_url, login_KeyUrl):    # 初始化数据
        self.Username = user
        self.Password = passwd
        nowTime = lambda:str(round(time.time() * 1000))
        self.now_time = nowTime()
        self.base_url=base_url
        self.login_url = login_url
        self.login_Key = login_KeyUrl
        
    def Get_indexHtml(self):    # 教务系统网站
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": self.login_url + self.now_time,
            "Upgrade-Insecure-Requests": "1"
        })
        self.response = self.session.get(self.login_url + self.now_time).content.decode("utf-8")

    def Get_csrftoken(self):    # 获取 csrftoken
        lxml = etree.HTML(self.response)
        self.csrftoken = lxml.xpath("//input[@id='csrftoken']/@value")[0]

    def Get_PublicKey(self):    # 获取公钥参数
        key_html = self.session.get(self.login_Key + self.now_time)
        key_data = json.loads(key_html.text)
        # print(self.login_Key + self.now_time)
        self.modulus = key_data["modulus"]
        self.exponent = key_data["exponent"]

    def Get_RSA_Password(self): # 生成公钥进行加密
        rsaKey = jw_visit.RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.modulus), HB64().b642hex(self.exponent))
        self.enPassword = HB64().hex2b64(rsaKey.encrypt(self.Password))

    def Longin_Home(self):  # post 登录, 返回 session 对象
        try:
            self.Get_indexHtml()
            self.Get_csrftoken()
            self.Get_PublicKey()
            self.Get_RSA_Password()
            login_data = [("csrftoken", self.csrftoken), ("yhm", self.Username), ("mm", self.enPassword)]
            login_html = self.session.post(self.login_url + self.now_time, data=login_data)
            if login_html.url.find("login_slogin.html") == -1:  # 根据 url 是否跳转判断是否登录成功
                print("Login success...")
        except:print("Login fail...")
        # except Exception as err:print(err)

    def get_lessons(self):  # 获取课表信息

        form_data = {
            'xnm': 2019,
            'xqm': 12
        }

        re = self.session.post(self.base_url + "/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151", data=form_data)
        re = re.json()
        #返回的信息：['kblx', 'xqbzxxszList', 'xsxx', 'sjkList', 'xkkg', 'xqjmcMap', 'xskbsfxstkzt', 'kbList', 'jxhjkcList', 'xsbjList']
        # print(re)

        xh=re['xsxx']['XH']#学号
        xm=re['xsxx']['XM']#姓名
        kbList=re['kbList']#课表
        allDic=dict()
        classDic=dict()
        for x in kbList:
            #'cd_id', 'cdmc', 'date', 'dateDigit', 'day', 'jc', 'jcor', 'jcs', 'jgh_id', 'jgpxzd', 'jxb_id', 'jxbmc', 'kch_id', 'kcmc', 'kcxszc', 'khfsmc', 'listnav', 'localeKey', 'month', 'oldjc', 'oldzc', 'pageable', 'pkbj', 'queryModel', 'rangeable', 'rsdzjs', 'sxbj', 'totalResult', 'userModel', 'xf', 'xkbz', 'xm', 'xnm', 'xqdm', 'xqh1', 'xqh_id', 'xqj', 'xqjmc', 'xqm', 'xqmc', 'xsdm', 'xslxbj', 'year', 'zcd', 'zhxs', 'zxs', 'zyfxmc']
            # print(x.values())
            jc=x['jcor']#节次
            xq=x['xqjmc']#星期
            try:classDic[xq].update({jc:[x['kcmc'],x['xm'],x['cdmc']]})#字典添加其他节次的课程信息
            except:classDic[xq]={jc:[x['kcmc'],x['xm'],x['cdmc']]}#为每周几建一个字典
        for i in classDic:
            print(i,classDic[i])#['1-2']

        print(classDic)
        # return

    def get_scores(self):   # 获取科目成绩信息

        form_data={
            'xnm': '',
            'xqm': '',
            '_search': 'false',
            'nd': 1602838874332,
            'queryModel.showCount': 100,
            'queryModel.currentPage': 1,
            'queryModel.sortName':None,
            'queryModel.sortOrder': 'asc',
            'time': random.randint(1,5) #查询次数
        }
        re = self.session.post(self.base_url + "/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005", data=form_data)
        re=re.json()
        return re

'''
上面的主要负责两个部分，可以跳过，不用深究
1. 登陆
2. 提供待查询的信息，包括课表、成绩
'''

# 主页
def index(request):
    return render(request,'index.html',locals())

# 成绩查询页
def scoresSearch(request):
    try:
        if request.method=="POST":

            # 登陆所需的几个参数
            user=request.POST.get("user","")
            passwd=request.POST.get("password","")
            base_url = "http://xjwgl.sziit.edu.cn/xtgl/login_slogin.html"
            login_url = base_url + "/xtgl/login_slogin.html?language=zh_CN&_t="  # 登录主页 url
            login_KeyUrl = base_url+"/xtgl/login_getPublicKey.html?time="  # 获取公钥参数的 url

            # 登陆，获取学生信息
            billie =Longin(user,passwd,base_url, login_url, login_KeyUrl)
            billie.Longin_Home()
            response=billie.get_scores()
            billie.get_lessons()
            items=response['items']
            print(items)

            # 存储各个科目的信息
            detailData=[]

            # 遍历添加各个科目的信息
            for i,item in enumerate(items):
                kcmc = item['kcmc'] #课程名称
                jsxm = item['jsxm'] #教师姓名
                kclbmc = item['kclbmc'] #课程类别
                cj = item['cj'] #成绩
                jd = item['jd'] #绩点
                xf = item['xf'] #学分
                xnmmc = item['xnmmc'] #学年
                s={'序号':i+1,'课程名称':kcmc,'教师姓名':jsxm,'课程类别':kclbmc,'成绩':cj,'绩点':jd,'学分':xf,'学年':xnmmc}
                detailData.append(s)

            # 平均绩点,取小数点后两位
            aveJd = round(sum([float(c['绩点']) for c in detailData])/len(detailData),2)

            if len(detailData)==0:
                msg="查询错误,请检查学号和密码是否正确"
        else:
            return redirect('/')
    except:
        msg="查询错误,请检查学号和密码是否正确"
    return render(request,'scoresSearch.html',locals())

