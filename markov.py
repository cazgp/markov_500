"""
This is a Python text mixer based on Markov analysis and is inspired by
`Section 13.8 of **How to think like a computer scientist ** <http://www.greenteapress.com/thinkpython/html/thinkpython014.html#toc149>`_.
"""
from __future__ import print_function

def parse_args():
    """
    Parse command line options and return an object with two attributes:
    `infiles`, a nonempty list of input file paths, and `outfile`, 
    a list of one output file path.
    """
    import argparse, textwrap, sys

    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter, 
      description=textwrap.dedent('''\
        A little command-line text mixer
      '''))
    parser.add_argument('infiles', nargs='+', 
      help='A list of text files to mix')
    # parser.add_argument('infiles', nargs='+', metavar='input_file',
    #   )
    parser.add_argument('-o', '--outfile', nargs='?', 
      type=argparse.FileType('w'), default=sys.stdout, 
      help='Output file (default: sys.stdout)')
    parser.add_argument('-n', '--num_words', nargs='?', type=int, default=500,
      help='Target number of words in output. Might be slightly more to end at the end of a sentence (default: 500)')    
    parser.add_argument('-r', '--ratios', nargs='?', 
      help='Mix ratios for the mix, e.g. 2,1,5 for 2 parts from the first file, 1 part from the second, and 5 parts from the third (default: equal parts from all files)')    
    return parser.parse_args()

def process_files(files, ratios):
    """
    Return a word list to do Markov analysis on.
    """
    texts = []
    for f in files:
        with open(f, 'r') as fin:
            texts.append(fin.read())
    if ratios:
        ratios = [int(r) for r in ratios.split(',')]
    else:
        ratios = [1 for i in texts]
    if len(ratios) != len(texts):
        ratios = [1 for i in texts]
    # Snip text files to accord with ratios
    R = sum(ratios)
    texts = [text.split() for text in texts]
    m = min(len(text) for text in texts)
    counts = [(r*m)//R for r in ratios]
    texts = [texts[i][:counts[i]] for i in range(len(texts))] 
    
    # Merge snippets
    return [word for text in texts for word in text]

def get_markov_analysis(words, prefix_length=2):
    r"""
    Return a Markov analysis of the list of strings ``words``.
    The output format is a dictionary with structure: 
    a tuple of contiguous words in ``words`` of length ``prefix_length`` 
    (a prefix) -> a list of all individual words in ``words`` that occur after
    that prefix.
    """
    words = tuple(words)
    d = {}
    for i in range(len(words) - prefix_length - 1):
        prefix = words[i:i + prefix_length]
        suffix = words[i + prefix_length]
        s = d.get(prefix,[])
        s.append(suffix)
        d[prefix] = s 
    return d
    
def get_random_text(words, num_words, prefix_length=2):
    r"""
    Return a text string of at least ``num_words`` random words from
    the given word list.
    Do this by shuffling ``d = get_markov_analysis(words, prefix_length)``,
    starting at the beginning of a sentence, and traversing ``d`` until 
    at least ``num_words`` random words have been generated and the end 
    of a sentence has been reached.
    """
    import random

    d = get_markov_analysis(words, prefix_length)
    
    # Start at the beginning of a random sentence
    prefixes = list(d.keys())
    random.shuffle(prefixes)
    t = list(prefixes[0])
    for prefix in prefixes:
        if prefix[0][0].isupper():
            t = list(prefix)
            break

    # Finish random text at the end of a sentence            
    end_of_sentence = False
    i = 0    
    while i < num_words or not end_of_sentence:
        prefix = tuple(t[i:i + prefix_length])
        s = d[prefix]
        suffix = random.choice(s)
        t.append(suffix)
        i += 1
        if suffix[-1] in ['.','?','!']:
            end_of_sentence = True
        else:
            end_of_sentence = False
    return ' '.join(t)

def main():
    args = parse_args()
    words = process_files(args.infiles, args.ratios)
    random_text = get_random_text(words, args.num_words)
    args.outfile.write(random_text)
    print()

if __name__ == "__main__":
    main()