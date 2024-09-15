import argparse
from pathlib import Path

from Varphi.frontend.helpers import execute

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Process input files and produce output.')
    
    # Define the arguments
    parser.add_argument('program', type=Path, help='Path to the program file')
    parser.add_argument('tape', type=Path, help='Path to the tape file')
    parser.add_argument('--output', type=Path, default=Path('output.vpt'), help='Path to the output file (default: output.vpt)')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Extract arguments
    programPath = args.program
    tapePath = args.tape
    outputPath = args.output
    
    execute(programPath, tapePath, outputPath)
    

if __name__ == '__main__':
    main()
