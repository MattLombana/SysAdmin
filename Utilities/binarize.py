#!/usr/bin/env python


def binarize(num):
    division = num / 2
    remainder = num % 2
    if (division == 0):
        return str(remainder)
    else:
        return binarize(division) + str(remainder)


if __name__ == '__main__':
    number = input('enter a number:\n')
    print binarize(number)
