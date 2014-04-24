def parse_args():
    import argparse, sys

    parser = argparse.ArgumentParser()

    parser.add_argument('allowed',
        type=argparse.FileType('rb'),
        help='A list of words')

    parser.add_argument('poem',
        type=argparse.FileType('rb'),
        help='A list of words')

    return parser.parse_args()

def verify(allowed, poem):
    from helpers import uniquify

    allowed_words = set(uniquify(allowed.read()))
    poem_words = set(uniquify(poem.read()))
    if not poem_words.issubset(allowed_words):
        print "Words in your poem that aren't allowed:"
        print ", ".join(poem_words.difference(allowed_words))

def main():
    args = parse_args()
    verify(args.allowed, args.poem)

if __name__ == "__main__":
    main()
