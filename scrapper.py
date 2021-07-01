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
    td_title = soup.find_all('td', attrs={'class':'title'})
    td_subtext = soup.find_all('td', attrs={'class':'subtext'})
    td_rank = soup.find_all('td', attrs={'class':'title', 'align':'right'})
    td_titleonly = [t for t in td_title if t not in td_rank]



    # writing to a file
    filename = "hackerNews.csv"
    f = open(filename,"w")
    headers  = "Rank, Title, Link, Source, Posted, Author, Score/n"



    # number of iterations
    num_iter = min(len(td_rank), len(td_subtext))


    # Extracting details

    for i in range(num_iter):

        Rank = td_rank[i].find('span', attrs={'class':'rank'})
        Title = td_titleonly[i].find('a', attrs ={'class':'storylink'})
       #Link = td_titleonly[i].find('a', attrs={'class':'storylink'})['href']
        Link = Title['href'] if Title and Title['href'].startswith('https') else 'https://news.ycombinator.com/'+Title['href']
        Source = td_titleonly[i].find('span', attrs={'class':'sitestr'})
        Posted = td_subtext[i].find('span', attrs={'class':'age'})
        Author = td_subtext[i].find('a', attrs={'class':'hnuser'})
        Score = td_subtext[i].find('span', attrs={'class':'score'})


        frame.append((Rank,Title,Link,Source,Posted,Author,Score))

        #f.write(Rank.replace(",","^")+","+Title.replace(",","^")+","+Link+","+Source.replace(",","^")+","+Posted+","+Author.replace(",","^")+","+Author.replace(",","^")+"\n")


        # writing to the file
        f.write(Rank.text.replace('.','') if Rank else 'Could not get article number')
        f.write(','+Title.text if Title else 'Could not get article title')
        f.write(','+Link if Link else 'No URL found for this article')
        f.write(','+Source.text if Source else 'https://news.ycombinator.com')
        f.write(','+Posted.text if Posted else 'Could not find when the article was posted')
        f.write(','+Author.text if Author else 'Could not get article author')
        f.write(','+Score.text if Score else 'Not Scored')
        
        f.write('\n')

    
    
    upperFrame.extend(frame)

f.close()


# visualizing dataframe using pandas

#data = pd.DataFrame(upperFrame, columns= ['Rank', 'Title', 'Link', 'Source', 'Posted', 'Author', 'Score'])
#data.head()





