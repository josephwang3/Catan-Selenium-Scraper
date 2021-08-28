from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# create path for Chrome driver and initialize the selenium webdriver
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

# open the website and print its title (name in tab)
driver.get('https://techwithtim.net')
print(driver.title)

"""
# find and click the Python Programming button
link = driver.find_element_by_link_text('Python Programming')
link.click()

# wait for, find, and click the Beginner Python Tutorials button and then the Get Started button
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Beginner Python Tutorials'))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'sow-button-19310003'))
    )
    element.click()

    article = driver.find_element_by_id('post-276')
    header = article.find_element_by_tag_name('h3')
    print(header.text)

except:
    driver.quit()
"""


# find the search box, and search for "test"
search = driver.find_element_by_name('s')
search.send_keys('test')
search.send_keys(Keys.RETURN)

# wait until the element located by id 'main' loads, which is the overall text box
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'main'))
    )

    articles = main.find_elements_by_tag_name('article')
    print(type(articles))
    for article in articles:
        header = article.find_element_by_class_name('entry-summary')
        print(type(article))
        print(header.text)

# finally executes regardless
finally:
    driver.quit()