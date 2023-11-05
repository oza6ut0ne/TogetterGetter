import argparse
import re
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def click(driver, element):
    driver.execute_script('arguments[0].click();', element)


parser = argparse.ArgumentParser()
parser.add_argument('url')
parser.add_argument('-o', '--one-by-one', action='store_true')
args = parser.parse_args()

if re.match(r'\d+', args.url):
    args.url = r'https://togetter.com/li/' + args.url

options = Options()
options.add_argument('--headless')
options.add_argument('--log-level=2')
driver = selenium.webdriver.Chrome(options=options)

driver.get(args.url)

while True:
    while True:
        try:
            more_tweet_btn = driver.find_element(By.ID, 'more_tweet_btn')
            click(driver, more_tweet_btn)
        except NoSuchElementException:
            break

    for tweet in driver.find_elements(By.CSS_SELECTOR, '.tweet_box .tweet'):
        print(tweet.text)
        input() if args.one_by_one else print()

    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, 'div.pagenation a[rel~=next]')
        click(driver, next_btn)
    except NoSuchElementException:
        break
