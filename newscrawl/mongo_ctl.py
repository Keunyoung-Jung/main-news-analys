import pymongo
import pandas as pd
from collections import Counter
from datetime import datetime
from newscrawl import MongoDB

time_arr = range(24)
time_dict = dict()

def get_dataframe(cursor) :
    return pd.DataFrame(list(cursor))

def today_feature(day=str(datetime.now()).split(" ")[0]):
    '''
    날짜를 지정하기 위해서 다음 형식에 따라서 파라미터 입력
    YYYY-MM-DD -> 2021-03-04
    '''
    for hour in time_arr :
        naver = f'naver_{day}T{hour}'
        
        naver_cursor = MongoDB.conn_mongodb(naver).find()
        time_dict[naver] = get_dataframe(naver_cursor)

def keyword_top10(df) :
    keyword_tmp = []
    for keyword in df['keywords'] :
        keyword_tmp += keyword
    counts = Counter(keyword_tmp)
    return [word[0] for word in counts.most_common(10)]

def press_top3(df) :
    return list(df['press'].value_counts().index[:3])

def get_mongo_data() :
    today_feature()
    ret_dict = dict()
    for date,df in time_dict.items() :
        if len(df) != 0 :
            ret_dict['KEYWORD_TOP10'] = keyword_top10(df)
            ret_dict['PRESS_TOP3'] = press_top3(df)
            
    return ret_dict