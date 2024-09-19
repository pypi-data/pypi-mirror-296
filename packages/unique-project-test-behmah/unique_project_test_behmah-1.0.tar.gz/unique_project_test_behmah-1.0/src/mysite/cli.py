# mysite/cli.py
import sys

def version():
    if len(sys.argv) > 1 and sys.argv[1] == '--version':
        print("mysite version 1.0")
    else:
        print("Usage: mysite --version")
