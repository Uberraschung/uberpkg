def line(string, separator, dic):
    key = ''
    values = []
    i = 0
    while(string[i] != separator):
        key += string[i]
        i += 1

    i += 2
    value = ''
    while(i < len(string)):
        value += string[i]
        if((string[i] == ' ' or i == len(string)-1) and value != ''):
            values.append(value.strip(' '))
            value = ''
        i += 1
    dic[key] = values

def line_list(lst, separator, dic):
    for i in lst:
        line(i, separator, dic)

def slackbuildscript(path):
    dic = {}
    with open(path, 'rt') as f:
        line = f.readline()
        while('PRGNAM' not in dic or 'VERSION' not in dic or 'BUILD' not in dic or 'TAG' not in dic):
            if(line[0] == '#' or line == '\n'):
                line = f.readline()
                continue
            s = line.split('=')
            if(s[0] == 'PRGNAM' or s[0] == 'VERSION' or s[0] == 'BUILD' or s[0] == 'TAG'):
                dic[s[0]] = s[1].strip()
            line = f.readline()
    clear = lambda string: string.split(':')[1].strip('}')
    filename = "%s%s-x86_64%s%s.tgz" % (dic['PRGNAM'], clear(dic['VERSION']), clear(dic['BUILD']), clear(dic['TAG']).strip('-'))
    return filename
    
if __name__ == '__main__':
    import sys
    slackbuildscript(sys.argv[1])
            