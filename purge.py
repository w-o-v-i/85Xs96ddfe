import shutil
import sys


def purge(path):
    shutil.rmtree(path)


if __name__ == "__main__":
    path = sys.argv[1]
    purge(path)
