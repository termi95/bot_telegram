#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from configparser import ConfigParser
import json
import os
import logic
import time
import downloadFrom
import sys
import repackage
repackage.up()
from db import db_query
config = ConfigParser()
config.read('/home/termi/bot_telegram/config.ini')


photoToDownload = {}
videoToSave = []

print('prepare chrome to work')
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
print('run chrome')
driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver', chrome_options = chrome_options)


for category in downloadFrom.websites:
    for url in downloadFrom.websites[category]:
        driver.get(url + '.json')
        time.sleep(1)
        res = driver.execute_script("return document.getElementsByTagName('pre')[0].innerHTML;")
        data = json.loads(res)
   	# Get array of photo to download
        if category not in photoToDownload:
            photoToDownload[category] = logic.getPhotoToDownload(data)
        else:
            photoToDownload[category] = photoToDownload[category] + logic.getPhotoToDownload(data)

        videoToSave = videoToSave + logic.getVideoToSave(data)            

driver.quit()



# download and save photo
print('download and save photo')
logic.savePhotoToFile(photoToDownload)

db_query.insertVideo(videoToSave)
#logic.saveVideoToFile(videoToSave, config.get('path', 'pathToRandomVideo'))