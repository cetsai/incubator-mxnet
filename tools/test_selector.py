import sys
import os
import argparse

def select_tests(file_name, func_name):
    tests = []
    
    if func_name.startswith("test_"):
        # select tests that have been directly changed
        tests.append((file_name, func_name))

    return tests

def find_dependents(dependencies, top, depth=1):
    dependents = dependencies

    if depth == 0:
        return dependents

    
    for root, dirs, files in os.walk(top):
        for f in files:
            #find  dependents in file
            pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("changes", nargs="*",
                        help="list of changed functions with file names")
    
    args = parser.parse_args()

    for change in args.changes:
        names = change.split(".")
        print(select_tests(names[0], names[1]))

