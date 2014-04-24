import re

def depunctuate(source, replacement=' '):
    return re.sub('[\(\)#.\n"\?,;:!-]', replacement, source)

def setted(source):
    setted = set(source)
    setted.remove('')
    return list(setted)

def uniquify(source):
    words = depunctuate(source).lower()
    return setted(words.split(' '))
