# importing libraries
import urllib.request
import sys
import time
from bs4 import BeautifulSoup,SoupStrainer
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
    only_td = SoupStrainer('td')
    soup = BeautifulSoup(page.content,'html.parser', parse_only=only_td)

    frame=[]



    # all links of news blogs listed on a page
    links = soup.find_all('td', attrs={'class':'title'})
    print(len(links))



    # writing to a file
    filename = "hackerNews.csv"
    f = open(filename,"w")
    headers  = "Rank, Title, Link, Source, Posted, Author, Score \n"



    # Extracting details

    for j in links:

        Rank = j.find('span', attrs={'class':'rank'}).text
        Title = j.find('a', attrs ={'class':'storylink'}).text.strip()
        Link = j.find('a', attrs={'class':'storylink'})['href'].strip()
        Source = j.find('span', attrs={'class':'sitestr'}).text.strip()
        Posted = j.find('span', attrs={'class':'age'}).text
        Author = j.find('a', attrs={'class':'hnuser'}).text
        Score = j.find('span', attrs={'class':'score'}).text


        frame.append((Rank,Title,Link,Source,Posted,Author,Score))

        f.write(Rank.replace(",","^")+","+Title.replace(",","^")+","+Link+","+Source.replace(",","^")+","+Posted+","+Author.replace(",","^")+","+Author.replace(",","^")+"\n")


    upperFrame.extend(frame)

f.close()


# visualizing dataframe using pandas

data = pd.DataFrame(upperFrame, columns= ['Rank', 'Title', 'Link', 'Source', 'Posted', 'Author', 'Score'])
data.head()





