import sys
import os
import argparse
import ast
import logging

logging.basicConfig(level=logging.DEBUG)

def find_dependents(dependencies, top, depth=1):
    dependents = set()

    if depth == 0:
        return dependents
    
    for root, dirs, files in os.walk(top):
        for f in files:
            dependents.update(find_dependents_file(dependencies))

    return find_dependents(dependents, depth-1)

def find_dependents_file(dependencies, filename):
    class CallVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            return node.id

        def visit_Attribute(self, node):
            return node.attr
            #try:
            #    return "{}.{}".format(node.value.id, node.attr)
            #except AttributeError:
            #    return "{}.{}".format(self.generic_visit(node), node.attr)

    with open(filename) as f:
        tree = ast.parse(f.read())
    logging.debug("seaching: %s", filename)

    dependents = dependencies.copy()
    cv = CallVisitor()
    
    for t in tree.body:
        if isinstance(t, ast.FunctionDef):
            name = t.name
        else:
            name = "top-level"

        for n in ast.walk(t):
            if isinstance(n, ast.Call):
                func = cv.visit(n.func)
                logging.debug("%s: %s called", name, func)
                if func in dependencies:
                    dependents.add(name)

    if dependents == dependencies:
        return dependents
    else:
        dependents.update(dependencies)
        return find_dependendts_file(dependents)


def output_results(dependents):
    logging.debug(dependents)


def parse_args():
    #class TestAction(argpase.Action):
    #    def __call__(self, parser, namespace, values, option_string=None):
    #        # get test name and file name
    #        return

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("changes", nargs="*",
        help="list of changed functions")
    
    arg_parser.add_argument("--path", "-p", default=".",
        help="file or directory in which to search for dependents")

    #arg_parser.add_argument("--")

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    
    #tests = select_tests(args.changes)    
    test = args.changes[0].split(":")
    for i in find_dependents_file([test[1]], test[0]):
        print(i)
    #output_results(tests)

