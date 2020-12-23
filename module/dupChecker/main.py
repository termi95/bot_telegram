#!/usr/bin/python3

from PIL import Image, ImageChops
from shutil import copyfile
from numba import njit
import os
import time

def deleteDuplicatedPhotos(photoToDel, path):
    for photo in photoToDel:
        os.remove(path + photo)

def getPhotoDiff(im1, im2):
    return ImageChops.difference(im1, im2)

def isTheSameSize(im1, im2):
    return im1.size == im2.size

@njit
def isTheSamePhoto(photo, checkingPhoto):
    return photo == checkingPhoto

def openImage(path, photo):
    return Image.open(path + photo)

def searchForDups(downloadedPhoto, path, progres = 1):
    photoToDel = []
    photoToCheck = downloadedPhoto    
    photosInFolder = len(downloadedPhoto)

    for photo in downloadedPhoto:
        print('progres: %' + str(format(progres/photosInFolder*100, '.2f')))
        if photo not in photoToDel:
            im1 = openImage(path, photo)
            for checkingPhoto in photoToCheck:
                im2 = openImage(path, checkingPhoto)  
                if not isTheSamePhoto(photo, checkingPhoto) and isTheSameSize(im1, im2):
                    diff = getPhotoDiff(im1, im2)
                    if not diff.getbbox():
                        if checkingPhoto not in photoToDel:
                            photoToDel.append(checkingPhoto)
        progres = progres + 1
    return photoToDel

def main():
    path = '/home/wspolne/termi/scraper/photo/memes/'
    downloadedPhoto = os.listdir(path)

    photoToDel = searchForDups(downloadedPhoto, path)
    
    print('number of deleted dups: ' + str(len(photoToDel)))
    if len(photoToDel) > 0:
        deleteDuplicatedPhotos(photoToDel, path)

main()