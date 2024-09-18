import argparse
from pathlib import Path

from .frontendHelpers import execute


def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser()

    # Define the arguments
    parser.add_argument('program',
                        type=Path,
                        help='Path to the program file')

    parser.add_argument('tape',
                        type=Path,
                        help='Path to the tape file')

    parser.add_argument('--output',
                        type=Path,
                        default=Path('output.vpt'),
                        help='Path to the output file (default: ./output.vpt)')

    # Parse the arguments
    args = parser.parse_args()

    # Extract arguments
    programPath = args.program
    tapePath = args.tape
    outputPath = args.output

    # Execute the program on the tape (output tape will be written here)
    execute(programPath, tapePath, outputPath)

    print("Successfully executed program")
    print(f"Output tape has been written to {outputPath}")


if __name__ == '__main__':
    main()
