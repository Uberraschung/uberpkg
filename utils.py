import urllib.request
from urllib.parse import urlparse

def download_http(url, apath='', fname=None):
    response = urllib.request.urlopen(url)
    print('Downloading from %s' % url)
    data = response.read()
    split = url.split('/')
    if not fname:
        filename = split[len(split)-1]
    else:
        filename = fname
    path = apath+filename
    with open(path, 'wb') as f:
        f.write(data)

    return path