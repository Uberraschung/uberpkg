import sys
from pymongo import MongoClient
from package import update, db_update, install, search

def usage():
    print('Invalid command. Usage:', file=sys.stderr)
    print('main.py install|update|search <package> ; Operates under a package', file=sys.stderr)
    print('main.py updatedb ; Updates the local database with slackbuilds\' data', file=sys.stderr)

def parsearg(args, collection):
    valid = ['update', 'install', 'search', 'updatedb']
    if len(args) < 1 or args[0] not in valid:
        usage()
    if args[0] == 'updatedb':
        update()
        db_update(collection)
    elif args[0] == 'install':
        install(collection, args[1])
    elif args[0] == 'search':
        dic = search(collection, args[1])
        for pkg in dic:
            desc = ' '.join(pkg['SLACKBUILD SHORT DESCRIPTION'])
            req = ' '.join(pkg['SLACKBUILD REQUIRES'])
            files = ' '.join(pkg['SLACKBUILD FILES'])
            print("\nNAME: %s\nVERSION: %s\nREQUIRES: %s\nSHORT DESCRIPTION: %s\nFILES: %s\n" % (pkg['SLACKBUILD NAME'][0], pkg['SLACKBUILD VERSION'][0], req, desc, files))


def main(args):
    client = MongoClient('localhost', 27017)
    db = client.slackbuilds
    collection = db.packages
    parsearg(args, collection)
    return 0

if __name__ == '__main__':
    main(sys.argv[1:])