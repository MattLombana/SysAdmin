#! /usr/bin/env python3

import argparse


def make_header(width, height, commentchar, space, line, prefix, postfix):
    endlines = commentchar * width
    blanklines = '{2}{0}{1}{0}{3}\n'.format(commentchar, space * (width - 2), prefix, postfix)


    neededspace = width - 2 - len(line)
    leftcenterspace = neededspace // 2

    if neededspace % 2 == 0:
        rightcenterspace = leftcenterspace
    else:
        rightcenterspace = leftcenterspace + 1

    num_blanklines = (height - 3) // 2

    titleline = '{4}{0}{1}{2}{3}{0}{5}'.format(commentchar, space * leftcenterspace, line, space * rightcenterspace, prefix, postfix)
    print(prefix + endlines + postfix)
    print(blanklines * num_blanklines, end = '')
    print(titleline)
    print(blanklines * num_blanklines, end = '')
    print(prefix + endlines + postfix)


def main():
    parser = argparse.ArgumentParser(description='Create a nice markdown heading')
    parser.add_argument('-w', help='How many characters wide', type=int, default=100)
    parser.add_argument('-t', help='How many lines tall', type=int, default='3')
    parser.add_argument('-s', help='Character for spacing comments', default=' ')
    parser.add_argument('-c', help='Character for denoting comments', default='#')
    parser.add_argument('--prefix', help='Prefix to print before each line', default='')
    parser.add_argument('--postfix', help='Postfix to print after each line', default='')
    parser.add_argument('lines', help='Strings to make into header', nargs='+')

    args = parser.parse_args()

    width = args.w  # width
    height = args.t  # height
    commentchar = args.c  # commentchar
    space = args.s  # space
    lines = args.lines
    prefix = args.prefix
    postfix = args.postfix

    for line in lines:
        make_header(width, height, commentchar, space, line, prefix, postfix)
        print('\n')



if __name__ == '__main__':
    main()
