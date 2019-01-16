from utils import download_http
from parser import line_list
from random import getrandbits
import tarfile
import os

def db_update(db):
    dic = {}
    lines = []
    localfile = open('SLACKBUILDS.TXT', 'rt')
    line = localfile.readline()
    while(line != ''):
        while(line != '\n'):
            lines.append(line.strip())
            line = localfile.readline()
        line_list(lines, ':', dic)
        db.insert_one(dic)
        dic.clear()
        lines[:] = []
        line = localfile.readline()
    localfile.close()

def update():
    url = 'https://ftp.slackbuilds.org/pub/slackbuilds/14.2/SLACKBUILDS.TXT'
    download_http(url)

def search(db, pkgname):
    dbs = db.find({"SLACKBUILD NAME": [pkgname]})
    return list(dbs)

def install(db, pkgname):
    dic = search(db, pkgname)
    required_list = dic[0]['SLACKBUILD REQUIRES'] 
    # If there are dependencies, recursive install 'em all
    if(required_list):
        for required_package in required_list:
            install(db, required_package)
    # Download package if there's no dependency