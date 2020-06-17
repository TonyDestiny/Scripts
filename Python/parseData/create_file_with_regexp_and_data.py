# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import re
import sys
import argparse
from json import dumps
from hashlib import md5

DIR_JSON = 'dir_json/'
REGEXP = r''
ERR_NONE = 'NONE'
ERR_FOUND = 'NOT_FOUND'
KEY_ONE = ""
KEY_TWO = ""
KEY_THREE = ""
FILE_EXTENSION = '.json'


def create_argparser():
    parser = argparse.ArgumentParser(
        prog='CreateFileWithRegexpAndData',
        description="""The script is intended for line-by-line reading of a files,
                       finding the necessary information in a line using regular expression
                       and generating a json file."""
    )
    parser.add_argument('-s', '--source', nargs='?', required=True, help='Files path.')

    return parser


def create_folder(folder_name):
    try:
        os.makedirs(folder_name)
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

    return True


def create_file(file_name):
    json_file = DIR_JSON + file_name + FILE_EXTENSION
    part = 1
    while True:
        if os.path.isfile(json_file):
            json_file = DIR_JSON + file_name + str(part) + FILE_EXTENSION
            part += 1
        else:
            return json_file


def create_string(id_obj, addr, data):
    return {KEY_ONE: id_obj, KEY_TWO: addr, KEY_THREE: data}


def trying_split(string):
    """
    Attempts to split a string by possible delimiters. 
    If it does not find a separator, it returns the whole string and the True flag.
    """
    try:
        split_line = string.split('----')
        split_line[1] = split_line[1].replace('\n', '').replace('\t', '')
        return split_line, False
    except:
        try:
            split_line = string.split(':', 1)
            split_line[1] = split_line[1].replace('\n', '').replace('\t', '')
            return split_line, False
        except:
            try:
                split_line = string.split('\t', 1)
                split_line[1] = split_line[1].replace('\n', '').replace('\t', '')
                return split_line, False
            except:
                try:
                    split_line = string.split(' ', 1)
                    split_line[1] = split_line[1].replace('\n', '').replace('\t', '')
                    return split_line, False
                except:
                    try:
                        split_line = string.split('|', 1)
                        split_line[1] = split_line[1].replace('\n', '').replace('\t', '')
                        return split_line, False
                    except:
                        try:
                            split_line = string.split(';', 1)
                            split_line[1] = split_line[1].replace('\n', '').replace('\t', '')
                            return split_line, False
                        except:
                            return string, True


def create_action(string):
    """
    It casts the string to the desired format.
    """
    node_id = md5(string.encode()).hexdigest()
    split_line, password_flag = trying_split(string)

    if password_flag:
        match = re.search(REGEXP, string)
        if match:
            action = create_string(node_id, match.group(0), string)
        else:
            action = create_string(node_id, ERR_FOUND, string)
    else:
        match = re.search(REGEXP, split_line[0])
        if match:
            action = create_string(node_id, split_line[0], split_line[1])
        else:
            match = re.search(REGEXP, split_line[1])
            if match:
                action = create_string(node_id, match.group(0), string)
            else:
                action = create_string(node_id, ERR_NONE, string)
    return action


def create_data(addr, file):
    """
    Writes json.
    """
    path_to_file = addr + '/' + file
    with open(path_to_file, 'r', errors='ignore') as origin_file:
        lines = origin_file.readlines()
        total_lines = len(lines)
        if total_lines < 1:
            print(f'File {path_to_file} is empty.')
            return
        json_file = create_file(file)
        with open(json_file, 'w') as jf:

            jf.write('[')
            jf.write(dumps(create_action(lines[0])))
            lines = set(lines[1:])
            for line in lines:
                jf.write(',')
                action = create_action(line)
                jf.write(dumps(action))
            jf.write(']')
            print(f'Total strings in file {path_to_file}: {total_lines}')
            print(f'Duplicates: {total_lines - len(lines) - 1}')


if __name__ == '__main__':
    parser = create_argparser()
    namespace = parser.parse_args(sys.argv[1:])
    path = namespace.source
    if not create_folder(DIR_JSON):
        print(f'Failed to create {DIR_JSON}')
        exit()
    for address, dirs, files in os.walk(path):
        for f in files:
            create_data(address, f)
