import sys
import os
import re

import pickle

def parse_fortunes(fortune_file):
    print("Parsing", fortune_file)
    category = os.path.basename(fortune_file)
    res = list()
    cur_text = ""
    cur_index = 0
    cur_fortune = None
    with open(fortune_file, "r") as fp:
        lines = fp.readlines()
    for line in lines:
        match = re.match("^%(\d+)$", line)
        if match:
            index = match.groups()[0]
            cur_index += 1
            if int(index) != cur_index:
                print(line)
                sys.exit("Expecting %i, got %s" % (cur_index, index))
            if cur_text:
                res.append(cur_text)
            cur_text = ""
        else:
            cur_text += line
    # last line: append the last fortune
    if cur_text:
        res.append(cur_text)
    return res

def main():
    root_dir = sys.argv[1]
    output = sys.argv[2]
    fortune_files = os.listdir(root_dir)
    fortune_files.sort()
    fortune_files = [x for x in fortune_files if not os.path.splitext(x)[1]]
    fortune_files.remove(".gitignore")
    fortune_files = [x for x in fortune_files if os.path.isfile(x)]
    fortune_files = [os.path.join(root_dir, x) for x in fortune_files]
    fortunes = dict()
    for fortune_file in fortune_files:
        fortunes[fortune_file] = parse_fortunes(fortune_file)
    with open(output, "wb") as fp:
        print("Dumping ...", end="")
        pickle.dump(fortunes, fp)
        print("ok")

if __name__ == "__main__":
    main()
