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
        if(string[i] == ' ' and value != '' or i == len(string)-1):
            values.append(value)
            value = ''
        i += 1
    dic[key] = values

def line_list(lst, separator, dic):
    for i in lst:
        line(i, separator, dic)