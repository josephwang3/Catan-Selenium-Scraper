from bs4 import BeautifulSoup
import requests

# Open html file and save it to an object
with open('simple.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

# Finds first <title> as attribute
match = soup.title.text
#print(match)

# Finds first <div>
match2 = soup.div
#print(match2)

# Finds <div class="footer">, need underscore after class because class is a special keyword in Python
match3 = soup.find('div', class_='footer') 
#print(match3)

# Finds <div class="article">
article = soup.find('div', class_='article')
#print(article)

# Gets the text of <a> under <h2> under the article
headline = article.h2.a.text
#print(headline)

summary = article.p.text
#print(summary)

# find_all() creates a list of all <div class="article">
for article in soup.find_all('div', class_='article'):
    headline = article.h2.a.text
    print(headline)
    
    summary = article.p.text
    print(summary)

    print()