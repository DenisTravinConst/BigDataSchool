#!/usr/bin/env python
"""mapper module"""
import urllib
RESPONSE = 'response'
INDEX_ERROR = 'indexError'
INPUT_FILES = '1.tsv,2.tsv'
OUTPUT_FILES = 'output.txt'
ERROR_FORMAT = 'error-{}XX'


def main():
    """main mapper method"""
    output_dict = dict()
    output_file = open(OUTPUT_FILES, 'r')
    for line in output_file:
        line_array = line.split('\t')
        output_dict[line_array[0]] = int(line_array[1])
    for file_path in INPUT_FILES.split(','):
        input_file = open(file_path, 'r')
        for line in input_file:
            if not line_analysis(output_dict, line):
                return False
    for key in output_dict:
        if output_dict[key] != 0:
            return False
    return True


def line_analysis(output_dict, line):
    """line analysis method"""
    line_array = line.split('\t')
    status_code = line_array[5].strip()
    if status_code == RESPONSE:
        return True
    elif status_code[0] != '2' and status_code[0] != '3':
        if ERROR_FORMAT.format(status_code[0]) in output_dict.keys():
            output_dict[ERROR_FORMAT.format(status_code[0])] -= 1
        else:
            return False
    else:
        try:
            url_root_array = line.strip().split('\t')[4].strip().split('/')
            url_root = url_root_array[0] + '/' + url_root_array[1]
            if urllib.unquote_plus(url_root) in output_dict.keys():
                output_dict[urllib.unquote_plus(url_root)] -= 1
            else:
                return False
        except IndexError:
            return False
    return True


if __name__ == '__main__':
    print 'Statistic validation result: {}'.format(main())
