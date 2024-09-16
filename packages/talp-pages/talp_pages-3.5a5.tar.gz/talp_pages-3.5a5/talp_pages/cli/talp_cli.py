#!/usr/bin/env python
import argparse
import logging

import talp_pages.pages as pages
import talp_pages.metadata as metadata
def main():
    parser = argparse.ArgumentParser(prog='talp', description='Command line tool of TALP-Pages.')
    subparsers = parser.add_subparsers(title='features' ,help="",dest='features')
 
    pages_parser = subparsers.add_parser('pages',help='Generate a collection of HTML pages.')
    metadata_parser = subparsers.add_parser('metadata',help='Add metdata to JSONS')
    pages.add_arguments(pages_parser)
    metadata.add_arguments(metadata_parser)
    
    
    
    args = parser.parse_args()

    
    if args.features == 'pages':
        pages.main(args)

    if args.features == 'metadata':
        metadata.main(args)

if __name__ == '__main__':
    main()
