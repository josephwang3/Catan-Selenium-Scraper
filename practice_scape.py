from selenium import webdriver
import time

# create path for Chrome driver and initialize the selenium webdriver
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

# open the website and print its title (name in tab)
driver.get('https://techwithtim.net')

time.sleep(2)

main = driver.find_element_by_id('main')
print(main.text)

header = main.find_element_by_class_name('panel-grid-cell').get_attribute('class')
print(header)

driver.quit()