import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
import time
import os
from tqdm import tqdm
import re
import mysql.connector
import random




##data 폴더 생성
try:
    if not os.path.exists("data"):
        os.mkdir("data")
except OSError:
    print ('Error: Creating directory. ' +  "data")


def cleand_text(text):

    # 별 제거
    text = text.replace('*', '')
    # 공백 삭제
    text = text.strip()

    return text



def make_urllist():
    page_num = 0
    first_url = ""
    urllist= []
    txtlist= []
    first_flag = 0
    last_flag = 0
    
    for i in range(100):
        url = 'https://finance.naver.com/sise/theme.naver?field=name&ordering=asc&page='+str(i+1)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        news = requests.get(url, headers=headers)

        # BeautifulSoup의 인스턴스 생성합니다. 파서는 html.parser를 사용합니다.
        soup = BeautifulSoup(news.content, 'html.parser')

        # CASE 1
        thema = soup.findAll(class_="col_type1")
        
        tma_list = []
        for i in range(1, len(thema)):
            #print(thema[i].text)
            tma_list.append(thema[i])
  
        #print(len(tma_list))

        
        
        # 각 뉴스로부터 a 태그인 <a href ='주소'> 에서 '주소'만을 가져옵니다.
        for idx, line in enumerate(tma_list):
            tmp_url = line.a.get('href')
            tmp_txt = line.text
            #바뀐페이지의 젓번째 url의 변동이없을때 탈출
            if idx == 0:
                if first_url == tmp_url:
                    first_flag = 1
                    break
                else:
                    first_url = tmp_url
            
            urllist.append(tmp_url)
            txtlist.append(tmp_txt)
            


        if first_flag == 1:
            break
        #뉴스 개수가 20개가 안되면 탈출
        if len(tma_list) < 40:
            break

        time.sleep(random.uniform(1.6,3.2))

    return urllist, txtlist





def find_thema(url):

    
    for i in range(1):
        url = 'https://finance.naver.com/'+url
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        news = requests.get(url, headers=headers)

        # BeautifulSoup의 인스턴스 생성합니다. 파서는 html.parser를 사용합니다.
        soup = BeautifulSoup(news.content, 'html.parser')

        # CASE 1
        thema = soup.findAll(class_="name_area")
        
        tma_list = []
        for  i  in range(len(thema)):
            tma_list.append(cleand_text(thema[i].text))

        time.sleep(random.uniform(1.6,3.2))

    return tma_list


thema_lists = {}

if __name__ == "__main__":

    url, txt = make_urllist()


    thema_lists = {}
    for idx, line in tqdm(enumerate(txt)):
        thema_lists[line]  =  find_thema(url[idx])


    with open('./data/themaju.json', 'w') as json_file:
        json.dump(thema_lists, json_file, ensure_ascii=False, indent=4)


