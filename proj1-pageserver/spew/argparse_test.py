import argparse

parser = argparse.ArgumentParser(
    description="Sample to test 'dest' for positional arg")
parser.add_argument("foo", dest="FOO", 
                        help="is this ok?")

    
