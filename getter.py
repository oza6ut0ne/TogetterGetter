import argparse
import pyquery
import re
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException


parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('-o', '--one-by-one', action='store_true')
args = parser.parse_args()

if re.match('\d+', args.url):
    args.url = r'https://togetter.com/li/' + args.url

try:
    options = Options()
    options.headless = True
    driver = selenium.webdriver.Chrome(chrome_options=options)
except WebDriverException:
    driver = selenium.webdriver.PhantomJS()

driver.get(args.url)

while True:
    while True:
        try:
            more_tweet_btn = driver.find_element_by_id('more_tweet_btn')
            more_tweet_btn.click()
        except NoSuchElementException:
            break

    pq = pyquery.PyQuery(driver.page_source)
    for tweet in pq.find('.tweet_wrap .tweet'):
        print(tweet.text, '\n')
        if args.one_by_one:
            input()

    try:
        next_btn = driver.find_element_by_css_selector('div.pagenation a[rel~=next]')
        next_btn.click()
    except NoSuchElementException:
        break
