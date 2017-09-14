import argparse

def main():
    parser = argparse.ArgumentParser(description='Search youtube Videos by Title, Description and/or Raw Filename')
    parser.add_argument("-t", "--title", help="pattern to search for in title", type=str)
    parser.add_argument("-d", "--description", help="pattern to search for in description", type=str)
    parser.add_argument("-f", "--file", help="pattern to search for in raw filename", type=str)
    args = parser.parse_args()
    if args.title:
        print ("title to search for <" + args.title + ">")
    if args.description:
        print ("description to search for <" + args.description + ">")
    if args.file:
        print ("title to search for <" + args.file + ">")

if __name__ == "__main__":
    main()