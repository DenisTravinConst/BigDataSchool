#!/usr/bin/env python
"""reducer module"""
import sys


def main():
    """main reducer method"""
    dirs = dict()
    for line in sys.stdin:
        key = line.strip().split('\t')[0].strip()
        count = line.strip().split('\t')[1].strip()
        if key in dirs:
            dirs[key] = int(dirs[key]) + int(count)
        else:
            dirs[key] = int(count)
    output(dirs)


def output(dirs):
    """reducer output method"""
    for key in dirs.keys():
        print '%s\t%s' % (key, dirs[key])


if __name__ == '__main__':
    main()