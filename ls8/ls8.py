#!/usr/bin/env python3
import curses

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()
'''
if __name__ == '__main__':
    curses.wrapper(cpu.run)
'''
