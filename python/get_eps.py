#! /usr/bin/python
# -- coding: utf-8 --
'''
Author: Brad Chou
Email: brad.chow@gmail.com
License: GPLv3
Develop on Python version: 2.7.17 
'''

import requests
import pandas as pd
import sys

#debug
LOG=0

if (len(sys.argv) == 2):
  NO = sys.argv[1]
  company = ""
  #To save EPS data
  EPS = []
  year_start = 96
  YEARS = [year_start, year_start+1, year_start+2, year_start+3, year_start+4, year_start+5, year_start+6, year_start+7, year_start+8, year_start+9, year_start+10, year_start+11]
  
  
  def financial_statement(year):
      global company
      global EPS
      
      if (year > 101):
          url = 'https://mops.twse.com.tw/mops/web/t163sb17'
          if (LOG == 1):
              print url
          r = requests.post(url, {
              'encodeURIComponent':1,
              'step':1,
              'firstin':1,
              'off':1,
              'queryName':'co_id',
              't05st29_c_ifrs':'N',
              't05st30_c_ifrs':'N',
              'inpuType':'co_id',
              'TYPEK':'all',
              'isnew':'false',
              'co_id':NO,
              'year':str(year)
          })    
            
          r.encoding = 'utf8'
          dfs = pd.read_html(r.text)[9]
          if (company == ""):
              company = (str)(dfs.iloc[0]).split(' ')[5]
              if (LOG==1): 
                  print company
          dfs = pd.read_html(r.text)[10]
          
          if (year == 107):
              if (LOG == 1):
                  print dfs.iloc[25]
                  print dfs.iloc[25, 1]
                  print dfs.iloc[25, 2]
                  print dfs.iloc[25, 3]
              EPS.append(dfs.iloc[25, 1])
              EPS.append(dfs.iloc[25, 2])
              EPS.append(dfs.iloc[25, 3])
          else:
              if (LOG == 1):
                  print dfs.iloc[23]
                  print dfs.iloc[23, 1]
                  print dfs.iloc[23, 2]
                  print dfs.iloc[23, 3]
              EPS.append(dfs.iloc[23, 1])
              EPS.append(dfs.iloc[23, 2])
              EPS.append(dfs.iloc[23, 3])
      else:
          url = 'https://mops.twse.com.tw/mops/web/t05st21'
          if (LOG == 1):
              print url
          r = requests.post(url, {
              'encodeURIComponent':1,
              'step':1,
              'firstin':1,
              'off':1,
              'queryName':'co_id',
              't05st29_c_ifrs':'N',
              't05st30_c_ifrs':'N',
              'inpuType':'co_id',
              'TYPEK':'all',
              'isnew':'false',
              'co_id':NO,
              'year':str(year)
          })    
            
          r.encoding = 'utf8'
          dfs = pd.read_html(r.text)[12]
          
          if (LOG == 1):
              print dfs.iloc[17]
              print dfs.iloc[17, 1]
              print dfs.iloc[17, 2]
              print dfs.iloc[17, 3]
          EPS.append(dfs.iloc[17, 1])
          EPS.append(dfs.iloc[17, 2])
          EPS.append(dfs.iloc[17, 3])
      
      
      return 1
               
  financial_statement(year_start+2)
  financial_statement(year_start+5)
  financial_statement(year_start+8)
  financial_statement(year_start+11)
  
  print "查詢公司：" + company
  print "YEAR\tEPS\t年成長率"
  count = 0
  while(count < 12):
      if (count > 0):
          if ((float)(EPS[count-1]) < (float)(0)):
              print (str)(YEARS[count]) + ":\t" + (str)(EPS[count]) + "\t%6.2f" % ((((float)(EPS[count])-(float)(EPS[count-1]))/(float)(EPS[count-1])*-100)) + "%"
          else:
              print (str)(YEARS[count]) + ":\t" + (str)(EPS[count]) + "\t%6.2f" % ((((float)(EPS[count])-(float)(EPS[count-1]))/(float)(EPS[count-1])*100)) + "%"
      else:
          print (str)(YEARS[count]) + ":\t" + (str)(EPS[count])
      count = count + 1
else:
    print "Usage: get_eps.py <台股號碼>"
    print "For example:"
    print "get_eps.py 2002"