#! -*- coding: utf-8 -*-

import os
import sys

ES_LOADER = 'elasticsearch_loader --index [] --progress --id-field [] --keys [] '

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} PATH')
        exit()
    else:
        for address, dirs, files in os.walk(sys.argv[1]):
            for file in files:
                print(f'LOADING {file}\n')
                os.system(ES_LOADER + address + '/' + file)
