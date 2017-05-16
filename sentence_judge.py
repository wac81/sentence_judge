# -*- coding:utf-8 -*-
'''
creater:arthur wu
create date:2017-05-16
details: score title for weixin and weibo

Unfinished:
1.crawler
2.hot news for extend words

'''
from __future__ import print_function
import os
import codecs
from tgrocery import Grocery
import jieba

def get_stopwords(file_stop_words = "stopwords.txt"):
    # 做常用词过滤
    # file_stop_words = "stopwords.txt"
    if os.path.exists(file_stop_words):
        stop_words = codecs.open(file_stop_words, encoding='UTF-8').read()
        return stop_words
    return False


class Phrasing:
    def __init__(self, model_name='sjudge'):
        self.model_name = model_name

    def get_phrasing_sets(self, title_path = 'title.csv'):
        '''
        train phrasing
        train sets: [(u'postive', text1),(u'negative',text2)]
        :param title_path:
        :return:
        '''
        # title_path = 'title.csv'
        if os.path.exists(title_path):
            with open(title_path, 'rb') as fp:
                lines = fp.readlines()[1:]

            postive = []
            negative = []
            all = []
            for line in lines:
                k = line.split(',')
                postive.append(k[1])
                negative.append(k[4])
                all.append((u'postive', k[1]))
                all.append((u'negative', k[4]))
            return all
        return None

    def train_phrasing_and_save(self, trainsets=all):
        '''

        :param trainsets:
        :param model_name:
        :return:
        '''
        try:
            grocery = Grocery(self.model_name)
            grocery.train(trainsets)
            grocery.save()
            return True
        except:
            return False

    def predict_phrasing(self, text = u'曾被年轻人嫌弃，如今却媲美Zara'):
        '''

        :param text:
        :param model_name:
        :return:
        '''
        new_grocery = Grocery(self.model_name)
        new_grocery.load()
        result = new_grocery.predict(text)
        return result.dec_values[u'postive']


class Hot_News_Words:
    '''
    get hot words from baidu/sogou/weibo
    '''
    def __init__(self):
        self.stop_words = get_stopwords()

    def get_baidu_words(self, baiduhot_path = 'baidu_hot.txt'):
        '''
         change to (every 24hrs)to get

         get hot words from baidu
        :param baiduhot_path:
        :return:
        '''
        if os.path.exists(baiduhot_path):
            with open(baiduhot_path, 'rb') as fp:
                lines = fp.read()
                hot_words = jieba.lcut(lines)
                hot_words = set(hot_words)

                hotwords = []
                for word in hot_words:
                    if word not in self.stop_words:# 做常用词过滤
                        # 判断词性加分
                        hotwords.append(word)
                return hotwords
        else:
            print ("热点文件不存在")
            return False

    def get_sogou_words(self):
        '''
        get hot words from sogou_weixin
        :return:
        '''
        return

    def get_weibo_words(self):
        '''
        get hot words from weibo
        :return:
        '''
        return

class Hot_News_Extend_Words:
    '''
    hot news for extend words
    '''
    def __init__(self):
        return


class Score_Title:
    def __init__(self, text):
        '''

        :param text: init text for title
        '''
        self.stop_words = get_stopwords()
        self.text = text

    def get_hot_score(self):
        hot_count = 0.0
        l_text = jieba.lcut(self.text)
        ltext = []
        baidu_hotwords = Hot_News_Words().get_baidu_words()

        for word in l_text:
            if word not in self.stop_words:  # 做常用词过滤
                # 判断词性加分
                ltext.append(word)

        for word in baidu_hotwords:
            if word in ltext:
                #判断词性加分
                hot_count += 3
        hot_score = hot_count/len(ltext)
        return hot_score

    def get_phrasing_score(self):
        phrasing_score = Phrasing().predict_phrasing(self.text)
        return phrasing_score

    def get_all_score(self):
        return self.get_phrasing_score()+self.get_hot_score()


class Crawler:
    '''
    :weibo
    http://s.weibo.com/top/summary?cate=realtimehot
    :weixin
    http://weixin.sogou.com/
    :baidu
    http://top.baidu.com/

    write sqlite db after crawler at 0:0 everyday or every 6 hours
    '''
    def __init__(self):
        return


    def baidu_crawler(self):
        # import requests
        # from bs4 import BeautifulSoup
        # import urllib
        #
        # # 基本Url
        # base_url = 'http://news.baidu.com/n?m=rddata&v=hot_word'
        # hot_type = '0'
        #
        # parameters = {'type': hot_type}
        #
        # # 获取 JSON 数据
        # r = requests.get(base_url, params=parameters)
        # print(r.url)
        #
        # hot_words_dict = r.json()
        #
        # # 输出热搜关键词
        # for hot_word in hot_words_dict.get('data'):
        #     print(hot_word.get('query_word'))
        return





if __name__ == "__main__":
    import sys

    while 1:
        # usr input
        print("Input Title: ", end='\b')
        input_msg = sys.stdin.readline()

        score = Score_Title(input_msg)
        # output
        print ("句式分数：", score.get_phrasing_score())
        print ("热点分数：", score.get_hot_score())
        print ("总分数：", score.get_all_score())
