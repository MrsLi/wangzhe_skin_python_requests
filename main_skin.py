# coding=utf-8
"""
王者荣耀皮肤图片爬取
"""
import requests
from bs4 import BeautifulSoup
import os

class Skin(object):
    def __init__(self):
        #英雄的列表的json地址
        self.hero_json = 'https://pvp.qq.com/web201605/js/herolist.json'

        #英雄详细列表页通用前缀
        self.base_url = 'https://pvp.qq.com/web201605/herodetail/'
        self.hero_details_url = ''

        # 图片存储文件夹
        self.img_folder = 'skin'
        # 图片url的通用前缀
        self.skin_url = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'
        self.skin_details_url =''

        #去除SSL安全警告
        requests.packages.urllib3.disable_warnings()

    def get_hero_list(self):
        request = requests.get(self.hero_json,verify=False)
        hero_list = request.json()
        return hero_list

    def get_hero_skin(self,hero_cname,hero_ename):
        self.hero_details_url=hero_ename+'.shtml'
        request = requests.get(self.base_url+self.hero_details_url,verify=False)
        request.encoding = 'gbk'
        html = request.text

        soup = BeautifulSoup(html,'lxml')
        skin_list  = soup.select('.pic-pf-list3')

        for skin_info in skin_list:
            img_names = skin_info.attrs['data-imgname']
            name_list = img_names.split('|')
            skin_no = 1
            for skin_name in name_list:

                self.skin_details_url = '%s/%s-bigskin-%s.jpg' % (hero_ename, hero_ename, skin_no)
                skin_no+=1
                # 下载图片到本地
                self.down_skin(hero_cname, skin_name + '.jpg')



    def down_skin(self,hero_cname,img_name):
        request = requests.get(self.skin_url+self.skin_details_url,verify=False)
        if request.status_code == 200:
            print('download-%s'%img_name)
            self.make_dir(self.img_folder+'/'+hero_cname)
            img_path = os.path.join(self.img_folder+'/'+hero_cname,img_name)
            with open(img_path,'wb') as img:
                img.write(request.content)
            print(img_name+'下载完成!')
        else:
            print(img_name+'error!')

    def make_dir(self,img_path):
        if not os.path.exists(img_path):
            os.mkdir(img_path)

    def run(self):
        self.make_dir(self.img_folder)
        hero_list = self.get_hero_list()
        for hero_info in hero_list:
            hero_ename =str(hero_info['ename'])
            hero_cname = hero_info['cname']
            self.get_hero_skin(hero_cname,hero_ename)

if __name__ == '__main__':
    skin= Skin()
    skin.run()








