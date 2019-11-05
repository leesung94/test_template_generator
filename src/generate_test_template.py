#!/usr/bin/python
import os.path
import sys

def handle_file(filehandle, filename):
    """
    The hard part
    """
    # Check if class or function
    

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

    if os.path.isfile(fileloc):
        filehandle = open(fileloc, "r")
        filename = os.path.basename(your_path)
    return filehandle

def closefile(filehandle):
    """
    Gotta remember to close the file handle
    """
    filehandle.close()

def main():
    [fileloc, filename] = handle_args()
    if fileloc == None:
        display_usage()
    else:
        filehandle = openfile(fileloc)
        lines = filehandle.readlines()
        closefile(filehandle)
        handle_file(lines, filename)
    return 0

if __name__ == "__main__":
    main()
