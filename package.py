from utils import download_http
from parser import line_list
from random import getrandbits
from shutil import copyfile
from subprocess import run
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
    # Download from https://ftp.slackbuilds.org/pub/slackbuilds/14.2/<packagename>.tar.gz
    path = download_http('https://ftp.slackbuilds.org/pub/slackbuilds/14.2'+dic[0]['SLACKBUILD LOCATION'][0].lstrip('.').rstrip('/')+'.tar.gz', 'pkgs/slackbuild/')
    tf = tarfile.open(path)
    tf.extractall('pkgs/slackbuild/')
    download = dic[0]['SLACKBUILD DOWNLOAD']
    if(not download or download[0] == 'UNSUPPORTED'):
        download = dic[0]['SLACKBUILD DOWNLOAD_x86_64']
    for src in download:
        download_http(src, 'pkgs/src/')
        slackbuild_dir = 'pkgs/slackbuild/'+dic[0]['SLACKBUILD NAME'][0]
        copyfile('pkgs/src/'+os.path.basename(src), slackbuild_dir+'/'+os.path.basename(src))
        print('Running %s' % dic[0]['SLACKBUILD NAME'][0])
        run([slackbuild_dir + '/' + dic[0]['SLACKBUILD NAME'][0] + '.SlackBuild'])