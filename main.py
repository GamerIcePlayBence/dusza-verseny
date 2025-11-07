from src import ui, test
import sys
from pathlib import Path

def main():
    if len(sys.argv) == 1:
        print("Használat: python script.py [--ui | <test_dir_path>]")
        sys.exit(1)

    if sys.argv[1] == "--ui":
        ui.UIMain()
    else:
        test.TESTMain(sys.argv[1])

if __name__ == "__main__":
    main()