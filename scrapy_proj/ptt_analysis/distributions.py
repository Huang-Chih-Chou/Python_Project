#!/usr/bin/python
#coding:utf-8
import json

from collections import defaultdict

import jieba
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from matplotlib.font_manager import FontProperties

sns.set(style='whitegrid')
# load ptt posts

path = 'gossip.json'

with open(path) as f:
    posts = json.load(f)
# get pushes

total_comments = defaultdict(int)
total_pushes = defaultdict(int)
total_hates = defaultdict(int)

for post in posts:
    for comment in post['comments']:
        user = comment['user']
        total_comments[user] += 1

        if comment['score'] > 0:
            total_pushes[user] += 1

        elif comment['score'] < 0:
            total_hates[user] += 1
#推文分析：每個推文者的推噓文次數(畫出排名最高一百名的推文者到底推了多少文。可以看到，大部分都是推文比較多，不過也有人幾乎都在噓文呢！)
def show_distributions(counts, pushes, hates):
    sorted_cnts = [t[0] for t in sorted(counts.items(), key=lambda x: -x[1])][:100]
    y = [counts[u] for u in sorted_cnts]
    y_pushes = [pushes[u] for u in sorted_cnts]
    y_hates = [hates[u] for u in sorted_cnts]
    x = range(len(y))

    f, ax = plt.subplots(figsize=(10, 6))

    sns.set_color_codes('pastel')
    sns.plt.plot(x, y, label='Total {}'.format('comments'), color='blue')
    sns.plt.plot(x, y_pushes, label='Total {}'.format('pushes'), color='green')
    sns.plt.plot(x, y_hates, label='Total {}'.format('hates'), color='red')

    ax.legend(ncol=2, loc='upper right', frameon=True)
    ax.set(ylabel='counts',#發表次數
           xlabel='people',#推文者
           title='Total comments')
    sns.despine(left=True, bottom=True)

    plt.show(f)
#用語分析：(利用結巴分詞，把每篇文章的詞收集起來，順便紀錄文章分數)
# display pushes
show_distributions(total_comments, total_pushes, total_hates)

# grap post
words = []
scores = []

for post in posts:
    d = defaultdict(int)
    content = post['content']
    if post['score'] != 0:
        for l in content.split('\n'):
            if l:
                for w in jieba.cut(l):
                    d[w] += 1
        if len(d) > 0:
            words.append(d)
            scores.append(1 if post['score'] > 0 else 0)
# grap comments
c_words = []
c_scores = []

for post in posts:
    for comment in post['comments']:
        l = comment['content'].strip()
        if l and comment['score'] != 0:
            d = defaultdict(int)
            for w in jieba.cut(l):
                d[w] += 1
            if len(d) > 0:
                c_scores.append(1 if comment['score'] > 0 else 0)
                c_words.append(d)
#convert to vectors(最後用 TfidfTransformer 做出特徵向量，配合 LinearSVC 進行預測訓練)
dvec = DictVectorizer()
tfidf = TfidfTransformer()
X = tfidf.fit_transform(dvec.fit_transform(words))

c_dvec = DictVectorizer()
c_tfidf = TfidfTransformer()
c_X = c_tfidf.fit_transform(c_dvec.fit_transform(c_words))

svc = LinearSVC()
svc.fit(X, scores)

c_svc = LinearSVC()
c_svc.fit(c_X, c_scores)

def display_top_features(weights, names, top_n, select=abs):
    font = FontProperties(fname=r"..\DroidFonts\DroidSansFallback.ttf", size=12)
    top_features = sorted(zip(weights, names), key=lambda x: select(x[0]), reverse=True)[:top_n]
    top_weights = [x[0] for x in top_features]
    top_names = [x[1] for x in top_features]

    fig, ax = plt.subplots(figsize=(10,8))
    ind = np.arange(top_n)
    bars = ax.bar(ind, top_weights, color='blue', edgecolor='black')
    for bar, w in zip(bars, top_weights):
        if w < 0:
            bar.set_facecolor('red')

    width = 0.30
    ax.set_xticks(ind + width)
    ax.set_xticklabels(top_names, rotation=45, fontsize=12, fontproperties=font)#fontdict={'fontname': 'Droid Sans Fallback', 'fontsize':12}

    plt.show(fig)
# top features for posts(貼文負向詞彙)
display_top_features(svc.coef_[0], dvec.get_feature_names(), 30)
# top positive features for posts(貼文正向詞彙)
display_top_features(svc.coef_[0], dvec.get_feature_names(), 30, select=lambda x: x)
# top features for comments(推文負向詞彙)
display_top_features(c_svc.coef_[0], c_dvec.get_feature_names(), 30)
# top positive features for comments(推文正向詞彙)
display_top_features(c_svc.coef_[0], c_dvec.get_feature_names(), 30, select=lambda x: x)