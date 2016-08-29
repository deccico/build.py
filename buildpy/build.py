#!/usr/bin/env python

import argparse
import logging


APP = "Build.py"
VERSION = '0.0.2'
DESCRIPTION = 'Pyhton build tool.'
LONG_DESCRIPTION = '"He must trust, and he must have faith. And so he builds, because what is building, and rebuilding and rebuilding again, but an act of faith?" Dave Eggers'

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=FORMAT,
                    #filename='out',
                    filemode='a'
                    )


#-------------------------------------------------------
def pre_build():
    pass


def main():
    # create the base parser with a subparsers argument
    parser = argparse.ArgumentParser(prog=APP.lower(), \
                                    description=DESCRIPTION)
    parser.add_argument('--version', action='version', version=APP + " " + VERSION)
    subparsers = parser.add_subparsers()
    
    parser_bewitch = subparsers.add_parser('pre-build checks', help='Runs any pre build checks required.')
    parser_bewitch.set_defaults(func=pre_build)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()


