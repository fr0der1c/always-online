import time
import os

import schedule
from selenium import webdriver

import credentials

lyric_generator = None


def get_lyric():
    lyrics = []
    n = 0
    with open('lyrics.txt') as f:
        for line in f:
            lyrics.append(line[0:len(line) - 1])
    while True:
        yield lyrics[n % len(lyrics)]
        n += 1


def check_and_login():
    # Show lyric
    global lyric_generator
    if lyric_generator is None:
        lyric_generator = get_lyric()
    print(next(lyric_generator))

    # Watch website
    exit_code = os.system('ping www.qq.com -c 1 -t 3')
    if exit_code:
        print('Network disconnected. Try to login.')
        driver = webdriver.Chrome()
        driver.get('http://172.16.0.101/')
        time.sleep(3)
        driver.find_element_by_id('username').send_keys(credentials.username)
        driver.find_element_by_id("pwd_tip").click()
        driver.find_element_by_id("pwd").send_keys(credentials.password)
        driver.find_element_by_id("loginLink").click()
    print('\n')


check_and_login()

schedule.every(30).seconds.do(check_and_login)

while True:
    schedule.run_pending()
    time.sleep(1)
