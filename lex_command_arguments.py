# Copyright 2015 [Brian Mc George]

import argparse


def manage_arguments():
    parser = argparse.ArgumentParser(
        description='Apply lexical analysis to input file')
    parser.add_argument('file_location', type=str, nargs=1,
                        help='the location of the input file')
    args = parser.parse_args()
    return args
