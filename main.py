import sys
from ftplib import FTP
from shutil import copyfile
from parser import line_list
import urllib.request
from urllib.parse import urlparse
import tarfile
import os
from tinydb import TinyDB, Query

def usage():
    print('Invalid command. Usage:', file=sys.stderr)

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
        db.insert(dic)
        dic.clear()
        lines[:] = []
        line = localfile.readline()
    localfile.close()

def update():
    ftp = FTP('ftp.slackbuilds.org')
    ftp.set_pasv(False)
    ret = ftp.login()
    print(ret)
    if ret != '230 Login successful.':
        print('Could not open slackbuild\'s FTP: %s' % ret, file=sys.stderr)
        sys.exit(1)
    try:
        copyfile('SLACKBUILDS.TXT', 'SLACKBUILDS.TXT.bkp')
    except FileNotFoundError:
        print('SLACKBUILDS.TXT doesn\'t exists yet.', file=sys.stderr)
    localfile = open('SLACKBUILDS.TXT', 'wb')
    ftp.retrbinary('RETR pub/slackbuilds/14.2/SLACKBUILDS.TXT', localfile.write)
    localfile.close()
    ftp.quit()

def search(pkgname, db):
    Pkg = Query()
    dbs = db.search(Pkg['SLACKBUILD NAME'][0] == pkgname)
    return dbs

def install(pkgname, db):
    dic = search(pkgname, db)
    for url in dic['SLACKBUILD DOWNLOAD']:
        response = urllib.request.urlopen(url)
        print('Downloading from %s' % url)
        data = response.read()
        split = url.split('/')
        filename = split[len(split)-1]
        path = '/tmp/'+filename
        with open(path, 'wb') as f:
            f.write(data)
        #tf = tarfile.open(path)
        #if not os.path.exists(path):
        #    os.makedirs(directory)
        #tf.extractall('')


def main(args):
    db = TinyDB('db.json')
    valid = ['update', 'install', 'search']
    if len(args) < 1 or args[0] not in valid:
        usage()
    if args[0] == 'update':
        db_update(db)
    elif args[0] == 'install':
        install(args[1], db)
    elif args[0] == 'search':
        dic = search(args[1], db)
        for pkg in dic:
            desc = ' '.join(pkg['SLACKBUILD SHORT DESCRIPTION'])
            req = ' '.join(pkg['SLACKBUILD REQUIRES'])
            files = ' '.join(pkg['SLACKBUILD FILES'])
            print("\nNAME: %sVERSION: %s\nREQUIRES: %s\nSHORT DESCRIPTION: %s\nFILES: %s\n" % (pkg['SLACKBUILD NAME'][0], pkg['SLACKBUILD VERSION'][0], req, desc, files))
    return 0

if __name__ == '__main__':
    main(sys.argv[1:])