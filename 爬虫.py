import requests
import json
import os
import time
import random

import jieba
import numpy as np
from  PIL import Image
import matplotlib.pyplot as plt
from wordcloud import  WordCloud


# 评论数据保持文件
comment_file_path = 'SKII_coment.txt'
#WC_MASK_IMG = 'SKII.jpg'
#WC_FONT_PATH = '/Library/Fonts/Songti.ttc'

def spider_comment(page=0) -> object:
    """爬虫京东商品评论"""
    url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=2574048&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1'%page
    kv = {'Referer': 'Referer: https://item.jd.com/2574048.html', 'ser-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        # print(r.text)
    except:
        print('爬取失败')
    # 拿到json数据
    r_json_str = r.text[20:-2]
   # print(r_json_str)
    # 转换成json类型
    r_json_obj = json.loads(r_json_str)
    #print(r_json_obj)
    # 获取评论列表数据
    r_json_comments = r_json_obj['comments']
    #print(r_json_comments)
    #将评论写到txt中
    for r_json_comment in r_json_comments:
        with open(comment_file_path,'a+') as file:
            file.write(r_json_comment['content']+'\n')
        #打印评论对象这种评论内容
        print(r_json_comment['content'])

def batch_spider_comment():
    """"
    批量爬取
    """
    if os.path.exists(comment_file_path):
        os.remove(comment_file_path)

    for i in range(10):
        spider_comment(i)
        time.sleep(random.random()*5)

def cut_word():
    """
    对数据分词
    """
    with open(comment_file_path) as file:
        coment_txt = file.read()
        wordlist = jieba.cut(coment_txt, cut_all=True)
        wl = "".join(wordlist)
        #print(wl)
        #return wl
#def create_word_cloud():
    # """
    # 生成云词
    # """
    #wc_mask = np.array(Image.open(WC_MASK_IMG))
        #wc = WordCloud(backgroud_color="white",max_words=2000,mask=wc_mask,scale=4,max_font_size=50,random_state=42)
        wc = WordCloud(background_color="white",font_path='msyh.ttc',width=1000,height=700)
        #wc.generate(cut_word())
        wc.generate(wl)
        wc.to_file("comment_word_clod.png")
    #plt.imshow(wc,interpolation="bilinear")
    #plt.axis("off")
    #plt.figure()
    #plt.show


if __name__ == '__main__':
    #batch_spider_comment()
    #生成词云
    #create_word_cloud()
    cut_word()