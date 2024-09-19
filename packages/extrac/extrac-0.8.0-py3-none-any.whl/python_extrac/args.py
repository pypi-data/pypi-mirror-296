import argparse


def make_argparser(prog="x"):
    parser = argparse.ArgumentParser(prog)
    parser.add_argument('filepath', help='archive file path')
    parser.add_argument('output', nargs="?", help='output file path')
    parser.add_argument('--encoding', default="utf-8", help='file encoding')
    return parser
