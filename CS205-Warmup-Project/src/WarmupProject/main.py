#!/usr/bin/env python
# Set project path and do django setup
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
from WarmupProject import djangoSetup
# Imports
from QueryInterface.QueryInterface import QueryInterface


def main():
    qi = QueryInterface()
    try:
        qi.run()
    except (KeyboardInterrupt, SystemExit):
        print()


if __name__ == "__main__":
    main()
