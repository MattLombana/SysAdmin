#! /usr/bin/env python3

import argparse


def make_header(width, commentchar, space, line):
    endlines = commentchar * width
    blanklines = '{0}{1}{0}'.format(commentchar, space * (width - 2))


    neededspace = width - 2 - len(line)
    leftcenterspace = neededspace // 2

    if neededspace % 2 == 0:
        rightcenterspace = leftcenterspace
    else:
        rightcenterspace = leftcenterspace + 1



    titleline = '{0}{1}{2}{3}{0}'.format(commentchar, space * leftcenterspace, line, space * rightcenterspace)
    print('{0}\n{1}\n{2}\n{1}\n{0}'.format(endlines, blanklines, titleline))


def main():
    parser = argparse.ArgumentParser(description='Create a nice markdown heading')
    parser.add_argument('-w', help='how many characters wide', type=int, default=100)
    parser.add_argument('-s', help='Character for spacing comments', default=' ')
    parser.add_argument('-c', help='Character for denoting comments', default='#')
    parser.add_argument('lines', help='Strings to make into header', nargs='+')

    args = parser.parse_args()

    width = args.w  # width
    commentchar = args.c  # commentchar
    space = args.s  # space
    lines = args.lines

    for line in lines:
        make_header(width, commentchar, space, line)
        print('\n')



if __name__ == '__main__':
    main()
