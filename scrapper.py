# importing libraries
import sys
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd






# Extracting data from a web page

# number of pages to which want to scrape
pagesToGet = 23


upperFrame = []


for page in range (0,pagesToGet+1):
    print('processing page : ', page)
    url = 'https://news.ycombinator.com/news?p=0'+str(page)


    try:
        page = requests.get(url)
        page.status_code

    except Exception as e:
        error_type, error_obj,error_info = sys.exc_info()
        print('Error for link : ',url) 
        print(error_type, 'Line : ',error_info.tb_lineno)
        continue

        
    #Delaing request time by 2 sec so that it doesn't load the server of the url
    time.sleep(2)


    # parsing html using beautifulSoup to pull data out of HTML and XML files
    soup = BeautifulSoup(page.content,'html.parser')

    frame=[]


    




