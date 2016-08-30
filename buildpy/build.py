#!/usr/bin/env python

import argparse
import logging
import os
import shutil
import subprocess
import sys
import time


APP = "Build.py"
VERSION = '0.1.0'
DESCRIPTION = 'Pyhton build tool.'
LONG_DESCRIPTION = '"He must trust, and he must have faith. And so he builds, because what is building, and rebuilding and rebuilding again, but an act of faith?" Dave Eggers'
PAUSE_SECONDS = 10
SHIP_FOLDER = "SHIP"

if sys.version_info <= (2, 4) or sys.version_info >= (3, 0):
    error = "ERROR: your Python version is not supported. Please use build.py with Python 2.7.x"
    print >> sys.stderr, error
    sys.exit(1)


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=FORMAT,
                    #filename='out',
                    filemode='a'
                    )


#-------------------------------------------------------
def run(cmd):
    logging.info("running: {0}".format(cmd))
    return subprocess.call(cmd, shell=True)

def pre_build_checks():
    logging.info("pre_build_checks checking...")
    modified_files = not run('git status -s|grep -E "^?M "')
    added_files = not run('git status -s|grep -E "^?A "')
    if modified_files:
        logging.warning("You have uncommited, modified changes in your git repo.")
    if added_files:
        logging.error("You have uncommited, added files in your git repo.")
    if modified_files or added_files:
        logging.warning("Pausing for {0} before continuing...".format(PAUSE_SECONDS))
    time.sleep(PAUSE_SECONDS)

def coverage():
    logging.info("running code coverage..")
    sys.exit(run("code_coverage_cmd"))

def build(type, clean, build_arg, unit_tests):
    logging.info("building... type:{0} clean:{1} build:{2} unit-test?:{3}".format(type, clean, build_arg, unit_tests))
    if clean:
        if os.path.isdir():
            logging.info("removing ship folder..")
            shutil.rmtree(SHIP_FOLDER)
    sys.exit(run("gcc {0} {1} {2} {3}".format(type, clean, build_arg, unit_tests)))

def validate_options(args):
    #subcommands are mandatory in Python 2.x therefore we need to implement our own validation..
    #this means we cannot call ./build.py -p or ./build.py -k alone. If we specify a subcommand, we must
    #call it.
    #When the issue below is fixed we could implement a positional argument (build?)
    # with -c -u and -b as optional arguments.
    # For more information: http://bugs.python.org/issue9253
    for opt in ['args.clean', 'args.build', 'args.unit_tests']:
        if args.type=='None' and eval(opt):
            raise RuntimeError("You need to specify the build type option (-t) along with --{0}".format(opt[5:]))

def main():
    parser = argparse.ArgumentParser(prog=APP.lower(), \
                                    description=DESCRIPTION)

    parser.add_argument('--version', action='version', version=APP + " " + VERSION)

    #-p section
    parser.add_argument("-p", "--pre_build_checks", default=False, action="store_true",
                        help="Runs any pre build checks required.")

    #-k code coverage section
    parser.add_argument("-k", "--coverage", default=False, action="store_true",
                        help="Coverage Reporting. Compiles binaries with coverage flags to generate "
                             "coverage and static analysis data for sonar.")

    #build section subcommand and options
    parser.add_argument("-t", "--type", type=str, default='None', choices=["debug", "prod", "profiling"],
                        help="Defines build flavor type.")
    parser.add_argument("-c", "--clean", default=False, action="store_true",
                        help="Deletes any meta files which are generated as part of a compile for given "
                             "type eg: intermediate object files and directories. Including delete the "
                             "existing SHIP folder. Must no delete non build generated files such as "
                             "source files not yet commited, etc.")
    parser.add_argument("-b", "--build", default=False, action="store_true",
                        help="Compiles the given target. All required binaries must be compiled, this included "
                             "all unit test binaries. All files must be put in the define structure.")
    parser.add_argument("-u", "--unit-tests", default=False, action="store_true",
                              help="Run all Unit tests from the defined unit-test deployment folder. "
                                   "If the unit test doesn't exit it should print a warning and compile "
                                   "(which will create the folder and binaries) then run the unit tests. "
                                   "All unit tests are required to produce a xml file in the root of the "
                                   "unit-test folder in junit xml format. One file per unit test binary is "
                                   "required. Naming convention is <name of unit-test-binary>- results.xml")

    args = parser.parse_args()

    validate_options(args)

    if args.pre_build_checks:
        pre_build_checks()

    if args.coverage:
        coverage()

    if args.type:
        build(args.type, args.clean, args.build, args.unit_tests)

if __name__ == "__main__":
    main()



