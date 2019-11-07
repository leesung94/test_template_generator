# test_template_generator

Usage:

The main application "generate_test_template.py" is located in the "src" folder.
To run the application on Windows type:
    python generate_test_template.py "path-to-m-file"

Note. This application supports Windows and Unix style paths. However the unit tests are written for Unix

This generates a test MATLAB script in the same directory as the source .m file.

Note. If the path argument contains spaces then enclose it in double quotes e.g.
    python generate_test_template.py "X:\some folder with spaces in its name\myScript.m"


Info:

To validate that your path is correct run it through "check_filepath.py" which is located in src.

To use this script type:
    python check_filepath.py "path-to-be-validated"