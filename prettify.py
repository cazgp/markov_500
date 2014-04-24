TAB = "{: >20}"

def parse_args():
    import argparse, sys

    parser = argparse.ArgumentParser()

    parser.add_argument('infile', nargs='?',
        type=argparse.FileType('rb'), default=sys.stdin, 
        help='A chunk of text in a file')

    parser.add_argument('-n', '--numcols',
        default=6, 
        type=int,
        help='Number of cols to print word list')

    parser.add_argument('-s', '--sort',
        action='store_true',
        help='Sort the words alphabetically')

    parser.add_argument('-r', '--rowwise',
        action='store_true',
        help='Print rowwise')

    return parser.parse_args()

def setify(infile, sort):
    from helpers import uniquify
    words = uniquify(infile.read())
    if sort: return sorted(words)
    return words

def rowwise(word_list, numcols):
    spare_words = num_words % numcols
    tabbed = TAB*numcols
    ret = ""

    for i in range(0, num_words, numcols):
        for j in range(0, numcols):
            try:
                ret += word_list[i+j]
            except: pass

    for i in range(0, num_words - spare_words, numcols):
        words = [word for word in word_list[i:i+numcols]]
        ret += tabbed.format(*words) + "\n"

    ret += (TAB*spare_words).format(*word_list[-spare_words:])
    return ret

def colwise(word_list, numcols):
    num_words   = len(word_list)
    spare_words = num_words % numcols
    numrows     = num_words / numcols

    if spare_words > 0:
        numrows += 1

    ret = ""

    for i in range(0, numrows):
        for j in range(0, num_words, numrows):
            total = i+j
            if total < num_words:
                ret += TAB.format(word_list[total])
        ret += "\n"

    return ret

def main():
    args = parse_args()
    word_list = setify(args.infile, args.sort)

    if args.rowwise:
        formatted = rowwise(word_list, args.numcols)
    else:
        formatted = colwise(word_list, args.numcols)

    print formatted

if __name__ == "__main__":
    main()
