#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile
from os import path
import sys
import shutil
from shutil import move
from shutil import make_archive
import argparse

DEST_FOLDER = 'result'
PATH_FOLDER = DEST_FOLDER + '/path'
ZIP_FOLDER = 'zip/'

def create_argparser():
    parser = argparse.ArgumentParser(
        prog='decomposing',
        description="""This script decomposes heavy folders
                        into small ones for futher upload to the server.
        """,
        epilog="""I would be grateful for your feedback."""
    )
    parser.add_argument('-n', '--name', required=True, help='Name of folder to be decompose.')
    parser.add_argument('-ms', '--maxsize', type=int, required=True, help='Max size output folder.')
    parser.add_argument('-mn', '--maxnum', type=int, required=True, help='Max number of files in output folder.')
    parser.add_argument('-z', '--zip', action='store_true', default=False,
                        help='Optional. If you want to archive output data, you may to use this flag.')

    return parser


def create_folder(name_path):
    try:
        os.makedirs(name_path)
    except FileExistsError:
        print(f"Folder {name_path} already exists.")
        answer = input("Do you want to continue? [Y/N]: ")
        while True:
            if answer == "N":
                return False
            elif answer == "Y":
                return True
            else:
                answer = input('Please enter "Y" or "N":')

    return True


def move_file(src, dst):
    try:
        move(src, dst)
    except MemoryError as f:
        print(f)
        print("Not enough disk space.")
        return False
    except PermissionError as f:
        print(f)
        print("Permission denied.")
        return False
    except NotADirectoryError as f:
        print(f)
        print("Not a directory.")
        return False
    return True


def result(move_data, total_data, folders):
    print(f"Files processed {move_data} out of {total_data}")
    print(f"Directory founded: {len(folders)}")


if __name__ == "__main__":

    bool_zip = False
    parser = create_argparser()
    namespace = parser.parse_args(sys.argv[1:])

    dirr = namespace.name
    ms = namespace.maxsize * 2 ** 20
    mn = namespace.maxnum

    try:
        tree = list(os.walk(dirr))
    except OSError:
        print(f"Could not access {dirr}.")
        exit()

    files = tree[0][2]
    folders = tree[0][1]
    total_data = len(files)
    move_data = 0
    number_part = 1
    name_path = PATH_FOLDER + str(number_part)
    if not create_folder(name_path):
        print(f"Failed to create {name_path}")
        exit()

    for file in files:
        if (path.getsize(name_path) >= ms) or (len(os.listdir(name_path)) == mn):
            number_part += 1
            name_path = PATH_FOLDER + str(number_part)
            if not create_folder(name_path):
                print(f"Failed to create {name_path}")
                result(move_data, total_data, folders)
                exit()
        if move_file(dirr + "/" + file, name_path):
            move_data += 1
        else:
            print("Work was suspended.")
            result(move_data, total_data, folders)
            exit()

    if namespace.zip:
        count_zip = 0
        try:
            create_folder(ZIP_FOLDER)
            list_dir = list(os.walk(DEST_FOLDER))[0][1]
            for fd in list_dir:
                try:
                    make_archive(ZIP_FOLDER + fd, "zip", DEST_FOLDER, fd)
                    count_zip += 1
                    print(f"{count_zip} out of {len(list_dir)} directories archived")
                except MemoryError:
                    print("Not enough disk space.")
                    print(f"Total directory archived {count_zip} out of {len(list_dir)}")
                    break
            print(f"Total directory archived {count_zip} out of {len(list_dir)}")
        except OSError:
            print("Failed.")

    result(move_data, total_data, folders)
    remove = input(f"Do you want to remove {dirr}? [y/n]: ")
    while True:
        if remove == 'y':
            try:
                shutil.rmtree(dirr)
                print("Removed success.")
                break
            except FileNotFoundError as f:
                print(f)
                print("Removed not success.")
                break
        elif remove == 'n':
            break
        else:
            remove = input("Please enter 'y' or 'n': ")
    
    remove = input(f"Do you want to remove {DEST_FOLDER} [y/n]: ")
    while True:
        if remove == 'y':
            try:
                shutil.rmtree(DEST_FOLDER)
                print("Removed success.")
                break
            except FileNotFoundError as f:
                print(f)
                print("Removed not success.")
                break
        elif remove == 'n':
            break
        else:
            remove = input("Please enter 'y' or 'n': ")
