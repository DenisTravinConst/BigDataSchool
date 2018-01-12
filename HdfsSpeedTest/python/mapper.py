#!/usr/bin/env python
"""mapper module"""
import sys
import urllib

RESPONSE = 'response'
INDEX_ERROR = "indexError"


def main():
    """main mapper method"""
    dirs = dict()
    for line in sys.stdin:
        try:
            line_array = line.strip().split('\t')
            status_code = line_array[5].strip()
            if status_code == RESPONSE:
                continue
            if status_code[0] != '2' and status_code[0] != '3':
                dir_set('error-' + status_code[0] + 'XX', dirs)
            else:
                url_root_array = line.strip().split('\t')[4].strip().split('/')
                url_root = url_root_array[0] + '/' + url_root_array[1]
                dir_set(urllib.unquote_plus(url_root), dirs)
        except IndexError:
            dir_set(INDEX_ERROR, dirs)
            continue
    output(dirs)


def dir_set(word, dirs):
    """directories set method"""
    if word in dirs:
        dirs[word] = int(dirs[word]) + 1
    else:
        dirs[word] = int(1)


def output(dirs):
    """mapper output method"""
    for key in dirs.keys():
        print '%s\t%s' % (key, dirs[key])


if __name__ == '__main__':
    main()