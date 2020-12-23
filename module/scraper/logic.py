 #!/usr/bin/python3
from termcolor import colored
from configparser import ConfigParser
import requests
import json
import os
config = ConfigParser()
config.read('/home/termi/bot_telegram/config.ini')


def getPhotoToDownload(data):
    photoToDownload = []
    # filtr .jpg from json
    for children in data["data"]["children"]:
        if("url" in children["data"]):
            if(children["data"]["url"] not in photoToDownload and children["data"]["url"].endswith(('.jpg'))):            
                photoToDownload.append(children["data"]["url"])

        if("link_url" in children["data"]):
            if(children["data"]["link_url"] not in photoToDownload and children["data"]["link_url"].endswith(('.jpg'))):            
                photoToDownload.append(children["data"]["link_url"])
    return photoToDownload

# download and save photo
def savePhotoToFile(photoToDownload):
    newPhotoCounter = 0
    path = '/home/wspolne/termi/scraper/photo/'
    for category in photoToDownload:
        
        #check if dir exist
        if not os.path.isdir(path + category):
            os.mkdir(path + category)   

        downloadedPhoto = os.listdir(path + category)

        for photo in photoToDownload[category]:
            if photo.rpartition('/')[-1] not in downloadedPhoto:
                response = requests.get(photo)

                file = open(path + category + "/" + photo.rpartition('/')[-1], "wb")
                file.write(response.content)
                file.close()
                newPhotoCounter += 1
    
    print(colored('download new photo:' + str(newPhotoCounter), config.get('termColor','OK')))
    
def getVideoToSave(data):    
    videoToDownload = []
    # filtr .jpg from json
    for children in data["data"]["children"]:
        post = children["data"]
        if( True == post['is_video']):                     
            videoToDownload.append(post["media"]["reddit_video"]["fallback_url"])
    return videoToDownload