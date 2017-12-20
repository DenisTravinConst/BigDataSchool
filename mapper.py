#!/usr/bin/env python
"""mapper module"""
import sys

URL_FIELD = "url"
URL_ROOT = "root"
INDEX_ERROR = "indexError"


def main():
    """main mapper method"""
    dirs = dict()
    for line in sys.stdin:
        try:
            url_word = line.strip().split('\t')[4].strip()
            if not url_word == URL_FIELD:
                url_root = url_word.split('/')[1].strip()
                if not url_root:
                    url_root = URL_ROOT
                if url_root in dirs:
                    dirs[url_root] = int(dirs[url_root]) + 1
                else:
                    dirs[url_root] = int(1)
        except IndexError:
            if INDEX_ERROR in dirs:
                dirs[INDEX_ERROR] = int(dirs[INDEX_ERROR]) + 1
            else:
                dirs[INDEX_ERROR] = int(1)
            continue
    output(dirs)


def output(dirs):
    """mapper output method"""
    for key in dirs.keys():
        print '%s\t%s' % (key, dirs[key])


if __name__ == '__main__':
    main()
