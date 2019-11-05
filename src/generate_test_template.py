#!/usr/bin/python
import os.path
import sys

def get_script_type(first_line):
    """
    Work out if we are dealing with a class or function script
    """
    is_class = True
    if "function" in first_line:
        is_class = False
    return is_class


def handle_file(lines, filename):
    """
    The hard part
    """

    # Check if class or function by inspecting first line in script
    first_line = lines[0]
    is_class = get_script_type(first_line)

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


def openfile(fileloc):
    """
    Open a file handle if the file exists, returns None otherwise
    """
    filehandle = None
    filename = None
    if os.path.isfile(fileloc):
        filehandle = open(fileloc, "r")
        filename = os.path.basename(fileloc)
    return [filehandle, filename]

def closefile(filehandle):
    """
    Gotta remember to close the file handle
    """
    filehandle.close()

def main():
    fileloc = handle_args()
    if fileloc == None:
        display_usage()
    else:
        [filehandle, filename] = openfile(fileloc)
        lines = filehandle.readlines()
        closefile(filehandle)
        handle_file(lines, filename)
    return 0

if __name__ == "__main__":
    main()
