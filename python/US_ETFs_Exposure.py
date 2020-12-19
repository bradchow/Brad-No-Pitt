#! /usr/bin/python
# -- coding: utf-8 --
'''
Author: Brad Chou
Email: brad.chow@gmail.com
License: GPLv3
Develop on Python version: 3.8.6
Install modules:
    requests: pip install requests 
    beautifulsoup4: pip install beautifulsoup4
'''

import sys
import requests
from bs4 import BeautifulSoup
import json
import urllib.request

#debug
LOG=0

#URL combination: A+B+PAGE
ETFDB_EXPOSURE_URL_A = "https://etfdb.com/stock/"
ETFDB_EXPOSURE_URL_B = "#etfs&sort_name=weighting&sort_order=desc&page="
ETFDB_EXPOSURE_URL_PAGE = "1"
ETFDB_JSON_URL_PAGE2_START = "https://etfdb.com/data_set/?tm=40274&cond={%22by_stock%22:"
ETFDB_JSON_URL_PAGE2_END = "}&no_null_sort=&count_by_id=true&limit=25&sort=weighting&order=desc&limit=25&offset="
ETFDB_JSON_URL_OFFSET = 25
KEYWORD_BY_STOCK = "by_stock"
KEYWORD_BY_STOCK_END = "}"
bContinue = 1
KEYWORD_ETF = "etf"
KEYWORD_ETF_END = "/"
HOLDINGS_URL = "https://etfdb.com/etf/"
HOLDINGS_URL_END = "/#holdings"


ticker = []
ticker_without_final_one =[]
etfs = []
found_etf = []
if LOG == 1:
    print (f'[DBG] {len(sys.argv)}')

count = 1
if (len(sys.argv) >= 3):
    print ("We will show you the ETFs with")
    
    while count <= len(sys.argv) - 1:
        print (f'({count}): {sys.argv[count]}')
        ticker.insert(count, sys.argv[count])
        if (count < len(sys.argv)-1):
            ticker_without_final_one.append(sys.argv[count])
        count = count + 1
    if LOG == 1:
        print (f'[DBG] ticker: {ticker[0:len(ticker)]}')
        for t in ticker_without_final_one:
            print(f'ticker_without_final_one: {t}')
    '''
    [1st step]
    Get last ticker and request to etfdb.com to get all ETFs which buy it
    '''
    url = (f'{ETFDB_EXPOSURE_URL_A}{sys.argv[len(sys.argv)-1]}')
    if LOG == 1:
        print (f'[DBG] url: {url}')
    
    r = requests.get(url)
    html_str = r.text
    if LOG == 1:
        print ('[DBG]')
        print(r.status_code)
        print(type(r))
        print(type(html_str))
    soup = BeautifulSoup(html_str, features="html.parser")
    if LOG == 1:
        print(f'[DBG] {soup.prettify()}')
        '''
        print(type(soup))
        print(soup.select("tbody"))
        print(tbody)
        '''
    tbody = soup.select("tbody")[0]
    trs = tbody.find_all('tr')
    if LOG == 1:
        print('Get:')
    for i in trs:
        if LOG == 1: 
            print(i.td.text)
        etfs.append(i.td.text)

    # get by_stock value
    table = soup.select("table")[0]
    if LOG == 1:
        print("table.data-url")
        print(table.get('data-url'))
    data_url = table.get('data-url')
    find_by_stock = data_url.find(KEYWORD_BY_STOCK)
    find_by_stock_end = data_url.find(KEYWORD_BY_STOCK_END, find_by_stock)    
    if find_by_stock == -1 or find_by_stock_end == -1:
        bContinue = 0
    if bContinue == 1:
        by_stock = data_url[find_by_stock+len(KEYWORD_BY_STOCK)+2:find_by_stock_end]
        if LOG == 1:
            print(by_stock)
    '''
    [2nd step]
    Get JSON data for this ticker from page 2 to the end
    '''
    page = 2
    while bContinue == 1:
        offset = ETFDB_JSON_URL_OFFSET * (page -1)
        url = (f'{ETFDB_JSON_URL_PAGE2_START}{by_stock}{ETFDB_JSON_URL_PAGE2_END}{offset}')
        if LOG == 1:
            print("url")
            print (url)
        json_data = urllib.request.urlopen(url).read().decode()
        if LOG == 1:
            y = json.dumps(json_data)
            print(y)
        y = json.loads(json_data)
        totalNum = len(y["rows"])
        if LOG == 1:
            print (f'rows: {len(y["rows"])}')
        if totalNum > 0:
            currentCount = 0
            while currentCount < totalNum:
                find_etf_name = y["rows"][currentCount]["symbol"].find(KEYWORD_ETF)
                find_etf_name_end = y["rows"][currentCount]["symbol"].find(KEYWORD_ETF_END, find_etf_name+len(KEYWORD_ETF)+1)
                if LOG == 1:
                    print (f'find_etf_name: {find_etf_name}, find_etf_name_end: {find_etf_name_end}')    
                if find_etf_name == -1 or find_etf_name_end == -1:
                    bContinue = 0
                if bContinue == 1:
                    etf_name = y["rows"][currentCount]["symbol"][find_etf_name+len(KEYWORD_ETF)+1:find_etf_name_end]
                    if LOG == 1:
                        print ('etf_name:')
                        print(etf_name)
                    etfs.append(etf_name)
                currentCount = currentCount + 1
        else:
            bContinue = 0
        page = page + 1    
              
    if LOG == 1:
        print(f'etfs:{len(etfs)}')
        '''
        for i in etfs:
            print(i)
        '''
    '''
    [3rd step]
    Iterator etfs and check it's holdings
    '''
    count = 1
    for etf in etfs:
        holdings = []
        url = (f'{HOLDINGS_URL}{etf}{HOLDINGS_URL_END}')
        if LOG == 1:
            print (f'[DBG] holdings url: {url}')
        r = requests.get(url)
        html_str = r.text
        if LOG == 1:
            print ('[DBG]')
            print(r.status_code)
            print(type(r))
            print(type(html_str))
        soup = BeautifulSoup(html_str, features="html.parser")
        if LOG == 1:
            print(f'[DBG] {soup.prettify()}')
            '''
            print(type(soup))
            print(soup.select("tbody"))
            print(tbody)
            '''
        tbody = soup.select("tbody")[2]
        trs = tbody.find_all('tr')
        if LOG == 1:
            print(f'({count}){etf} holdings:')
        for tr in trs:
            if LOG == 1: 
                print(tr.td.text)
            holdings.append(tr.td.text)
        bPass = 1
        for t in ticker_without_final_one:
            try:
                holdings.index(t)    
            except:
                bPass = 0
                if LOG == 1:
                    print("Unexpected error:", sys.exc_info()[0])
                break
        if bPass == 1:
            print(f'found etf: {etf}')
            found_etf.append(etf)
        count = count + 1

    print(f'number of found_etf: {len(found_etf)}')
    for f in found_etf:
        print(f)

else:
    print ("Usage: US_ETFs_Exposure.py <US ticker symbol> <US ticker symbol>")
    print ("For example:")
    print ("US_ETFs_Exposure.py AAPL TSLA COST")