#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from subprocess import call

SPLIT_DIR = 'split_data/'
CMD = 'split -a 3 -d -l '
PART_FILE = '.part'
FILE_NAME = 'split_file'


def create_parser():
    parser = argparse.ArgumentParser(
        prog='Split data',
        description="""Script for split your data.
                       It uses bash command "split" """
    )
    parser.add_argument('-p', '--path', nargs='?', required=True, help='Files path')
    parser.add_argument('-l', '--lines', default='1000000', help='put NUMBER lines per output file')
    return parser


def create_folder(folder_name):
    try:
        os.makedirs(folder_name)
        return True
    except FileExistsError:
        print(f'Folder {folder_name} already exists.')
        answer = input('Do you want to continue? [y/n]: ')
        while True:
            if answer == 'n':
                return False
            elif answer == 'y':
                return True
            else:
                answer = input('Please, enter "y" or "n": ')


def create_file(changer):
    output_file = SPLIT_DIR + FILE_NAME + str(changer) + PART_FILE
    part = 1
    while True:
        if os.path.isfile(output_file):
            output_file = SPLIT_DIR + FILE_NAME + str(changer) + str(part) + PART_FILE
            part += 1
        else:
            return output_file


def create_cmd(src, split, lines):
    return f'{CMD} {lines} {src} {split}'


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if not create_folder(SPLIT_DIR):
        print(f'Failed to create {SPLIT_DIR}')
        exit()
    changer = 0
    for address, dirs, files in os.walk(namespace.path):
        for f in files:
            path_to_source = address + '/' + f
            path_to_split = create_file(changer)
            os.system(create_cmd(path_to_source, path_to_split, namespace.lines))
            changer += 1
