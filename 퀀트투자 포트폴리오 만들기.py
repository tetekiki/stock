#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Chapter 7. 크롤링을 위한 웹 기본지식


# In[8]:


import requests as rq

url = 'https://quotes.toscrape.com/'
quote = rq.get(url)

print(quote)


# In[11]:


quote.content[:1000]


# In[13]:


from bs4 import BeautifulSoup

quote_html = BeautifulSoup(quote.content, 'html.parser')
quote_html.head()


# In[16]:


quote_div = quote_html.find_all('div',class_= 'quote')
quote_div[0]


# In[21]:


quote_span = quote_div[0].find_all('span', class_='text')
quote_span


# In[23]:


quote_span[0].text


# In[40]:


quote_div = quote_html.find_all('div',class_='quote')
[i.find_all('span',class_='text')[0].text for i in quote_div]


# In[43]:


quote_text= quote_html.select('div.quote > span.text')

quote_text


# In[44]:


quote_text_list = [i.text for i in quote_text]
quote_text_list


# In[47]:


quote_author= quote_html.select('div.quote > span> small.author')

quote_author_list = [i.text for i in quote_author]

quote_author_list


# In[48]:


quote_link = quote_html.select('div.quote > span > a')
quote_link


# In[ ]:


#Chapter 9. 동적 크롤링과 정규 표현식


# In[6]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# In[8]:


url= 'https://www.naver.com/'
driver.get(url)
driver.page_source[1:1000]


# In[15]:


driver.find_element(By.LINK_TEXT, value= '뉴스').click()


# In[19]:


driver.switch_to.window(driver.window_handles[1])
driver.close()


# In[20]:


import re

p = re.compile('[a-z]+')
type(p)


# In[21]:


m =  p.match('python')
print(m)


# In[22]:


m.group()


# In[ ]:


# 10 국내주식 데이터 수집


# In[1]:


import requests as rq
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/sise/sise_deposit.nhn'
data = rq.get(url)
data_html = BeautifulSoup(data.content)
parse_day = data_html.select_one(
    'div.subtop_sise_graph2 > ul.subtop_chart_note > li > span.tah').text

print(parse_day)


# In[8]:


import keyring

keyring.set_password('tiingo', 'tetekiki', 'e189f79ef29beeab746c567e1af2577ca0c52974')


# In[10]:


from tiingo import TiingoClient
import pandas as pd
import keyring

api_key = keyring.get_password('tiingo', 'tetekiki')
config = {}
config['session'] = True
config['api_key'] = api_key
client = TiingoClient(config)


# In[11]:


tickers = client.list_stock_tickers()
tickers_df = pd.DataFrame.from_records(tickers)

tickers_df.head()


# In[12]:


s_df.groupby(['exchange', 'priceCurrency'])[''].count()


# In[17]:


import yfinance as yf
import pandas as pd

tickers = ['^KS11', '039490.KS'] 

all_data = {}
for ticker in tickers:
    all_data[ticker] = yf.download(ticker,
                                   start="2016-01-01",
                                   end='2021-12-31') 
    
prices = pd.DataFrame({tic: data['Close'] for tic, data in all_data.items()})
ret = prices.pct_change().dropna()


# In[24]:


prices


# In[25]:


ret


# In[26]:


import statsmodels.api as sm

ret['intercept'] = 1
reg = sm.OLS(ret[['039490.KS']], ret[['^KS11', 'intercept']]).fit()


# In[27]:


reg.summary()


# In[28]:


print(reg.params)


# In[34]:


import pandas_datareader.data as web
from pandas_datareader.famafrench import get_available_datasets

datasets = get_available_datasets()
datasets[1:20]


# In[46]:


import pandas_datareader.data as web

df_pbr = web.DataReader('Portfolios_Formed_on_BE-ME',
                        'famafrench',
                        start='1900-01-01')
df_pbr[0].head()


# In[51]:


import matplotlib.pyplot as plt
from matplotlib import cm

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

df_pbr_vw = df_pbr[0].loc[:, ['Lo 20', 'Qnt 2', 'Qnt 3', 'Qnt 4', 'Hi 20']]
df_pbr_cum = (1 + df_pbr_vw / 100).cumprod()
df_pbr_cum.plot(figsize=(10, 6),
                colormap=cm.jet,
                legend='reverse',
                title='PBR별 포트폴리오의 누적 수익률')
plt.show()


# In[52]:


import numpy as np

df_pbr_cum = np.log(1+df_pbr_vw/100).cumsum()
df_pbr_cum.plot(figsize=(10, 6),
                colormap=cm.jet,
                legend='reverse',
                title='PBR별 포트폴리오의 누적 수익률')
plt.show()


# In[53]:


import pandas as pd

def factor_stat(df):

    n = len(df)

    ret_ari = (df / 100).mean(axis=0) * 12
    ret_geo = (1 + df / 100).prod()**(12 / n) - 1
    vol = (df / 100).std(axis=0) * np.sqrt(12)
    sharp = ret_ari / vol

    stat = pd.DataFrame(
        [ret_ari, ret_geo, vol, sharp],
        index=['연율화 수익률(산술)', '연율화 수익률(기하)', '연율화 변동성', '샤프지수']).round(4)

    stat.iloc[0:3, ] = stat.iloc[0:3, ] * 100

    return stat


# In[54]:


factor_stat(df_pbr_vw)


# In[58]:


n = len(df_pbr_vw)
ret_geo = (1 + df_pbr_vw / 100).prod()**(12 / n) - 1
ret_geo


# In[60]:


vol = (df_pbr_vw / 100).std(axis=0) * np.sqrt(12)
vol


# In[61]:


import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

df_mom = web.DataReader('10_Portfolios_Prior_12_2',
                        'famafrench',
                        start='1900-01-01')
df_mom_vw = df_mom[0]
df_mom_cum = np.log(1 + df_mom_vw / 100).cumsum()

plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

df_mom_cum.plot(figsize=(10, 6),
                colormap=cm.jet,
                legend='reverse',
                title='모멘텀별 포트폴리오의 누적 수익률')
plt.show()


# In[1]:


import keyring

# 종합계좌
keyring.set_password('real_app_key', '@2378932', 'PS4qGwCdYH0mjZl6bLDisGKt1Afzvqya5jgq')
keyring.set_password('real_app_secret', '@2378932', 'yRS6mF0X68cGGr/2/lSmStmh4Uc+Gftp12kU+ooOadrJ8LVmxsWleodJv/7JroMjzBxDUrIiBLTZtyAu7MtjN+6BITwhluuBPFetY7cijqHnSn+Di3XxECgMhrpt+xhNkX33E2Pc/Gwqe/wQtnKkAZ79JA+RcmrTTbC8n66zY1j7YpFBeQo=')

# 모의계좌
keyring.set_password('mock_app_key', '@2378932', 'PScPti4PiDQWxW5q5YV96RQWQi6OX9Yx6Wvs')
keyring.set_password('mock_app_secret', '@2378932', 'i5cEPPFctgUJNMz4w/yrBKfDvpHbYBNUQ04/iNOuF20GkK6VrXWIKmFdpJDQhNH8BWa0p/xM2mA4s4qVcqc8sWEHfO8TRqKDj6pJf+Ps6O7FXhBBKgV7cSGD6b/rqoiWIt1I1dDTKk5hGYaY0GVMv70Phga6vAnxXV5MLhM8RMnim10/pNY=')


# In[15]:


import requests
import json
import keyring

# key
app_key = keyring.get_password('mock_app_key', '@2378932')
app_secret = keyring.get_password('mock_app_secret', '@2378932')

# base url
url_base = "https://openapivts.koreainvestment.com:29443" # 모의투자

# information
headers = {"content-type": "application/json"}
path = "oauth2/tokenP"
body = {
    "grant_type": "client_credentials",
    "appkey": app_key,
    "appsecret": app_secret
}

url = f"{url_base}/{path}"
print(url)


# In[16]:


res = requests.post(url, headers=headers, data=json.dumps(body))
access_token = res.json()['access_token']


# In[18]:


def hashkey(datas):
    path = "uapi/hashkey"
    url = f"{url_base}/{path}"
    headers = {
        'content-Type': 'application/json',
        'appKey': app_key,
        'appSecret': app_secret,
    }
    res = requests.post(url, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]

    return hashkey


# In[19]:


path = "uapi/domestic-stock/v1/quotations/inquire-price"
url = f"{url_base}/{path}"

headers = {
    "Content-Type": "application/json",
    "authorization": f"Bearer {access_token}",
    "appKey": app_key,
    "appSecret": app_secret,
    "tr_id": "FHKST01010100"
}

params = {"fid_cond_mrkt_div_code": "J", "fid_input_iscd": "005930"}

res = requests.get(url, headers=headers, params=params)
res.json()['output']['stck_prpr']


# In[21]:


path = "/uapi/domestic-stock/v1/trading/order-cash"
url = f"{url_base}/{path}"

data = {
    "CANO": "50114201",  # 계좌번호 앞 8지리
    "ACNT_PRDT_CD": "01",  # 계좌번호 뒤 2자리
    "PDNO": "005930",  # 종목코드
    "ORD_DVSN": "01",  # 주문 방법
    "ORD_QTY": "10",  # 주문 수량
    "ORD_UNPR": "0",  # 주문 단가 (시장가의 경우 0)
}

headers = {
    "Content-Type": "application/json",
    "authorization": f"Bearer {access_token}",
    "appKey": app_key,
    "appSecret": app_secret,
    "tr_id": "VTTC0802U",
    "custtype": "P",
    "hashkey": hashkey(data)
}

res = requests.post(url, headers=headers, data=json.dumps(data))
res.json()


# In[22]:


import datetime

def job():
    print(datetime.datetime.now().strftime('%H:%M:%S'))    
    print("=====================")


# In[24]:


import schedule

schedule.every(3).seconds.do(job)


# In[25]:


schedule.get_jobs()


# In[26]:


while True:
    schedule.run_pending()

