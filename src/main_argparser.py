import argparse
import sys
import os
new_wd = os.getcwd()

def mainParsArgs(arg):
    parser = argparse.ArgumentParser(description="testing...")
    parser.add_argument('--data_source', help='data source', default=new_wd + '/src/data/data.xlsx')
    parser.add_argument('--name', help='name', default='Jane Dough')
    parser.add_argument('--strip_id', help='strip_id', default='x000001')
    parser.add_argument('--value', help='value', default='101')
    parser.add_argument('--which_test', help='1 or 2', default='test1')
    return parser.parse_args(arg)

my_args = mainParsArgs(sys.argv[1:])
#*****************begin reading arguments
data_source = my_args.data_source
name = my_args.name
strip_id = my_args.strip_id
value = my_args.value
which_test = my_args.which_test
#*****************end reading arguments
