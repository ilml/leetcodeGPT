"""
main file to call the UnitTestGenerator.py
"""

import argparse
from UnitTestGenerator import UnitTestGenerator

def main():
    parser = argparse.ArgumentParser(description='args for UnitTestGenerator')

    parser.add_argument('--start', '-S', help='starting number of the questions')
    parser.add_argument('--end', '-E', help='ending number of the questionss')
    parser.add_argument('--model', '-M', help='model to use', default="text-davinci-003")

    args = parser.parse_args()

    for question in range(int(args.start), int(args.end) + 1):
        UnitTestGenerator(str(question), args.model).generate_unit_test()

if __name__ == "__main__":
    main()
