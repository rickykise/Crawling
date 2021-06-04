import json
import pymysql,time,datetime
import requests,re
from elasticsearch import Elasticsearch, helpers
from pynori.korean_analyzer import KoreanAnalyzer

# def create_index(index):
#     if not es.indices.exists(index=index):
#         return es.indices.create(index=index)

def create_index(body):
    if not es.indices.exists(index=index):
        return es.indices.create(index=index, body=body)

def insert(body):
    return es.index(index=index, doc_type=doc_type, body=body)

def search(index, data):
    if data is None:
        data = {'match_all': {}}
    else:
        data = {'match': data}
    body = {'query': data}
    res = es.search(index=index, body=body)
    return res

if __name__=='__main__':
    # url = '127.0.0.1';port = '9200';index = 'news';doc_type = 'daum'
    #
    # es = Elasticsearch(f'{url}:{port}')
    #
    # sr = search(index, None)
    # print(sr)
    # with open('setting.json', 'r', encoding='utf-8') as f:
    #     setting = json.load(f)
    #
    # print(setting)
    #
    # create_index(setting)
    # print(es.indices.get_settings(index))

    # body = {
    #     'analyzer': 'content',
    #     'text': '매일 비가 오네요.'
    # }
    #
    # r = es.indices.analyze(index=index, body=body)
    # print(r)

    # r = create_index(index)

    # data = {
    #     'date': '202008112229',
    #     'category': 'cyw',
    #     'newspaper': 'KBS',
    #     'title': '큰 비 온다는 경보에도 수영등산 처벌은?',
    #     'content': '집중호우와 산사태 경보가 내려졌는데도, 입산이 통제된 산에 올라가거나 바다에서 수영을 즐기던 동호회원들이 적발되거나 구조됐습니다.',
    #     'url': 'https://news.v.daum.net/v/20200811222929678'
    # }
    # ir = insert(data)

    # print(sr)
    nori = KoreanAnalyzer(decompound_mode='DISCARD', # DISCARD or MIXED or NONE
                          infl_decompound_mode='DISCARD', # DISCARD or MIXED or NONE
                          discard_punctuation=True,
                          output_unknown_unigrams=False,
                          pos_filter=False, stop_tags=['JKS', 'JKB', 'VV', 'EF'],
                          synonym_filter=False, mode_synonym='NORM') # NORM or EXTENSION
    print(nori.do_analysis("가벼운 냉장고")['termAtt'])
    # print(nori.do_analysis("아빠가 방에 들어가신다."))
    # r = requests.get(link, headers=headers)
