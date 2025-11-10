#!/usr/bin/python3

import sys
import os
import argparse
import json

def validate_file(rules_file):
    if os.path.isfile(rules_file):
        try:
            with open(rules_file, 'r') as file:
                json.load(file)
            print("Routing rules sucessfully tested")
        except ValueError as e:
            print("Invalid JSON: %s" % e)
            sys.exit(1)
    else:
        # Shouldn't happen because the calling script tests for the existence first.
        print("'%s' isn't a file" % rules_file)
        sys.exit(1)

if __name__ == '__main__':
    validate_file("_data/routingrules.json")
