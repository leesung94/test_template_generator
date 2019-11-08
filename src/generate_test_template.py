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
        inst_cont_extr.get_script_type()

        # Get all function declarations except first declaration if script is a 
        # function and not a class
        if len(inst_cont_extr.get_functions()) == 0:

            # Nothing to generate
            print("Error : No body functions detected in script")
            return 1
        else:
            # Generate Start of test script
            inst_scri_gene = sg.Script_Generator(
                inst_cont_extr.filename, 
                inst_cont_extr.directory)

            inst_scri_gene.generate_file_head()

            # Search contents for function declarations
            #   function templates - one per function
            for func in inst_cont_extr.function_names:
                inst_scri_gene.generate_function_block(func)

            # Generate end of file
            inst_scri_gene.generate_file_tail()

            # Create test template in same directory as content script then write and close
            inst_scri_gene.write_file()
            return 0
    else:
        print("Error: Could not open file. Please ensure path is correct")
        return 1

def display_usage():
    print("Error: Expecting path of the file which will be templated")

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
