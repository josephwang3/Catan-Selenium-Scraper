import requests
from bs4 import BeautifulSoup

url = 'https://www.bseindia.com/corporates/Forth_Results.aspx'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}

source = requests.get(url, headers=headers).text
soup = BeautifulSoup(source, 'lxml')

page = 1
while page <= 3:
    print(page)
    rows = soup.select('.TTRow')

    # print some data to screen:
    for tr in soup.find_all('tr', class_='TTRow'):
        print(tr.get_text(strip=True, separator=' '))
    
    # get the data located in <input name="..." value ="..."> tags
    d = {}
    for i in soup.find_all('input'):
        d[i['name']] = i.get('value', '')
    
    # delete some data parameters
    if 'ctl00$ContentPlaceHolder1$btnSubmit' in d:
        del d['ctl00$ContentPlaceHolder1$btnSubmit']
    
    # set correct page
    page += 1
    d['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$gvData'
    d['__EVENTARGUMENT'] = f'Page${page}'

    soup = BeautifulSoup(requests.post(url, headers=headers, data=d).text, 'lxml')