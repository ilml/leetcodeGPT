"""
Main file to call the leetcodeGPT.py

@tom 2023-08-22
"""

import argparse
from leetcodeGPT import leetcodeGPT

def main():
    parser = argparse.ArgumentParser(description='args for leetcodeGPT')

    parser.add_argument('--start', '-S', help='starting number of the questions')
    parser.add_argument('--end', '-E', help='ending number of the questionss')
    parser.add_argument('--debug', '-D', help='number of debugs', default=0)
    parser.add_argument('--history', '-H', help='length of history', default=0)
    parser.add_argument('--model', '-M', help='model to use', default="text-davinci-003")

    args = parser.parse_args()

    for question in range(int(args.start), int(args.end) + 1):
        leetcodeGPT(str(question), int(args.debug), int(args.history), args.model).solve()

if __name__ == "__main__":
    main()
