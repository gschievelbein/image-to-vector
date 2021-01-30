import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', help='Folder with images', required=True)

    args = parser.parse_args()

    files = os.listdir(args.folder)
    ids = [os.path.splitext(file)[0] for file in files]
    del files

    with open(args.folder + '.txt', 'w') as file:
        for id in ids:
            file.write("%s\n" % id)


if __name__ == '__main__':
    main()
