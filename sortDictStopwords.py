import re


sortStopwords = input('sort stopwords?(y/n)') in 'Yy'
removeDictDup = input('remove duplicate words in userdict?(y/n)') in 'Yy'

def appendDict(key, weight=None, part=None):
    if key not in dict:
        element = [set(),set()]
        if weight != None:
            element[0].add(weight)
        if part != None:
            element[1].add(part)
        dict[key] = element
    else:
        if weight != None:
            dict[key][0].add(weight)
        if part != None:
            dict[key][1].add(part)

if sortStopwords:
    with open('stopwords.txt', 'r') as f:
        stopwords = list(set([word.strip('\n ') for word in f.readlines()]))
    stopwords.sort(key=lambda x:len(x))
    with open('stopwords.txt', 'w') as f:
        f.write('\n'.join(stopwords))
dict = {}

if removeDictDup:
    re_userdict = re.compile('^(.+?)( [0-9]+)?( [A-Za-z]+)?$', re.U)
    finalResult = ''
    with open('userdict.txt', 'r') as f:
        words = f.readlines()
        for word in words:
            word = word.strip()
            if word == '':
                continue
            key, weight, part = re_userdict.match(word).groups()
            if weight is not None:
                weight = weight.strip()
            if part is not None:
                part = part.strip()
            appendDict(key, weight, part)
        for key, (weight, part) in dict.items():
            weight = list(weight)
            part = list(part)
            w = ''
            p = ''
            if len(weight) > 1:
                weightIndex = int(input(f'{key} has multiple weights, which to keep?(input 1-based index)\n{weight}\n'))-1
                w = weight[weightIndex]
            elif len(weight) == 1:
                w = weight[0]
            if len(part) > 1:
                partIndex = int(input(f'{key} has multiple parts, which to keep?(input 1-based index)\n{part}\n'))-1
                p = part[partIndex]
            elif len(part) == 1:
                p = part[0]
            finalResult+='\n'+key
            if w != '':
                finalResult+=' '+w
            if p != '':
                finalResult+=' '+p
    with open('userdict.txt', 'w') as f:
        f.write(finalResult)

