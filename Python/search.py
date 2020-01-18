#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from elasticsearch import Elasticsearch
import argparse


def create_argparser():
    parser = argparse.ArgumentParser(
        prog='searcher',
        description="""This script helps you search Elasticsearch.
                       It is best to pre-configure the search for your specific request.
                       Just pass the dictionary with the necessary settings to the "body" parameter on line 25.
        """
    )
    parser.add_argument('-s', '--source', nargs='?', required=True, help='desired value.')
    parser.add_argument('-i', '--index', required=True, help='The index in which to search.')

    return parser


if __name__ == '__main__':
    parser = create_argparser()
    namespace = parser.parse_args(sys.argv[1:])
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    res = es.search(index=namespace.index,
                    body={"query": {
                        "query_string": {
                            "query": namespace.source
                        }
                    }
                    })

    for item in res['hits']['hits']:
        print(item['_source'])
