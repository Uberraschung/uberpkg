import sys
from ftplib import FTP
from shutil import copyfile
from parser import line_list
import urllib.request
from urllib.parse import urlparse

def usage():
    print('Invalid command. Usage:', file=sys.stderr)

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

def search(pkgname):
    dic = {'SLACKBUILD NAME': ['']}
    lines = []
    localfile = open('SLACKBUILDS.TXT', 'rt')
    line = localfile.readline().strip()
    while(True):
        while(line != ""):
            lines.append(line)
            line = localfile.readline().strip()
        line_list(lines, ':', dic)
        if(dic['SLACKBUILD NAME'][0] != pkgname):
            lines[:] = []
            line = localfile.readline().strip()
            dic = {'SLACKBUILD NAME': ['']}
        else:
            break
    localfile.close()
    return dic

def install(pkgname):
    dic = search(pkgname)
    #SLACKBUILD DOWNLOAD
    for url in dic['SLACKBUILD DOWNLOAD']:
        response = urllib.request.urlopen(url)
        print('Downloading from %s' % url)
        data = response.read()
        split = url.split('/')
        filename = split[len(split)-1]
        with open('/tmp/'+filename, 'wb') as f:
            f.write(data)


def main(args):
    valid = ['update', 'install', 'search']
    if len(args) < 1 or args[0] not in valid:
        usage()
    if args[0] == 'update':
        update()
    elif args[0] == 'install':
        install(args[1])
    elif args[0] == 'search':
        dic = search(args[1])
        desc = ' '.join(dic['SLACKBUILD SHORT DESCRIPTION'])
        req = ' '.join(dic['SLACKBUILD REQUIRES'])
        files = ' '.join(dic['SLACKBUILD FILES'])
        print("""
        NAME: %s
        VERSION: %s
        REQUIRES: %s
        SHORT DESCRIPTION: %s
        FILES: %s
        """ % (dic['SLACKBUILD NAME'][0], dic['SLACKBUILD VERSION'][0], req, desc, files))
    return 0

if __name__ == '__main__':
    main(sys.argv[1:])