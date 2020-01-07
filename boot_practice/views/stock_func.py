from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re 
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

max_past_day = 5
def main(request):
    item_list=[]
    end_list = []
    sub_list = []
    result_list =[]
    nums = request.POST["text"]
    url = "https://kabuoji3.com/stock/"+nums+"/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15 "
    }
    soup = BeautifulSoup(requests.get(url, headers = headers).content, 'html.parser')
    items = soup.find_all('td')
    for app in items:
        item_list.append(app.text.split()[0])

    times = len(item_list)//7-1
    #終値のリストを作成
    for i in range(times):
        end_list.append(int(item_list[6 + i*7]))
    #変化値のリストを作成
    len_end = len(end_list)
    for i in range (len_end-1):
        sub_result = end_list[i]-end_list[i+1]
        sub_list.append(sub_result)
        if sub_result >=0:
            result_list.append([1])
        else:
            result_list.append([0])
    del result_list[294:]
    for i in range (len_end - max_past_day):
        #各日においてmax_past_dayまで過去の値動きを遡るリストを作成
        result_list[i].extend(sub_list[i+1:i+int(max_past_day)])
    for a in result_list:
        a.reverse()
    #機械学習用dataframe作成
    df = pd.DataFrame(data=result_list)


    X= df.iloc[0:,0:3].values
    y=df.iloc[0:,4].values
    print
    def check_tree(max_depth):
        X_train, X_test, y_train, y_test = train_test_split(X,y, stratify = y,test_size =0.3,shuffle=True, random_state =10)
        forest=RandomForestClassifier(n_estimators=1,max_depth=max_depth,class_weight="balanced")
        forest.fit(X_train,y_train)
        return forest, forest.predict(X_test),forest.score(X_train, y_train), forest.score(X_test, y_test),forest.feature_importances_

    score_trains = {}
    score_tests = {}
    imp ={}
    predictions = {}

    for max_depth in range(1,20):
        _, prediction ,score_train, score_test,importance = check_tree(max_depth)
        score_trains[max_depth] = score_train
        score_tests[max_depth] = score_test
        imp[max_depth] = importance
        predictions[max_depth] = prediction
    test_key = max(score_tests,key=score_tests.get) 
    resu = [score_trains[test_key],score_tests[test_key],imp[test_key],predictions[test_key],test_key]






        

    

    

    return render(request,'result.html',{"nums":resu})