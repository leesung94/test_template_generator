#!/usr/bin/python

# Author:
#   Lee Sung

# Libraries
import sys

# User Defined
import script_generator as sg

def handle_file(fileloc):
    """
    The hard part
    """

    # Get details and contents of the file
    inst_cont_extr = sg.Contents_Extractor(fileloc)

    # Check we opened the file
    if inst_cont_extr.open_file() == 0:

        # Read contents then close file
        inst_cont_extr.read_contents()
        inst_cont_extr.close_file()

        # Check if class or function by inspecting first line in script
        is_class = inst_cont_extr.get_script_type()

        # Generate Start of test script

        # Search contents for function declarations
        #   function templates - one per function

        # Generate end of file

        # Create test template in same directory as content script

        # Write and close
    else:
        return 1

def display_usage():
    print "Error: Expecting path of the file which will be templated"

def handle_args():
    """
    Parse the command line arguments, we expect 2. Firstly this script then
    the path to the file that will be templated
    """
    fileloc = None
    if len(sys.argv) == 2:
        fileloc = sys.argv[1]
    return fileloc

def main():
    fileloc = handle_args()
    if fileloc == None:
        display_usage()
    else:
        handle_file(fileloc)
    return 0

if __name__ == "__main__":
    main()
