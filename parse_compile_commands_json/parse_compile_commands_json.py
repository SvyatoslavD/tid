#!/usr/bin/env python3

import pprint
import json

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

filename = input("Please enter the path to your file: ")
data = read_json_file(filename)

directory = {}
command = {}
file = {}

keys = ["directory", "command", "file"]
dicts = [directory, command, file]

defines = []
options = []
includes = []
unknown = []

for command in data:
    for key, dict in zip(keys, dicts):
        if key == "command":
            lk = "file"
        else:
            lk = key

        if not dict.get(command[lk]):
            dict[command[lk]] = 1
        else:
            dict[command[lk]] += 1

        if key != "command":
            continue

        lc = command[key].split(" ")
        # CMake's commands args:
        # [0] = compiler (gcc)
        # [1:-4] = flags
        # [-4:] = -o filename.o -c filename.c
        lc = lc[1:-4]

        for flag in lc:
            flag.strip()

            # skip bullshit
            if flag.startswith("-O") or flag == "" or flag == "-ggdb" or flag.endswith("_EXPORTS"):
                continue

            if flag.startswith("-D"):
                if not flag in defines:
                    defines.append(flag)
                continue

            if (flag.startswith("-W") or flag.startswith("-f")):
                if not flag in options:
                    options.append(flag)
                continue

            if flag.startswith("-I"):
                if not flag in includes:
                    includes.append(flag)
                continue

            if not flag in unknown:
                unknown.append(flag)
                continue

#pprint.pprint(directory)
#pprint.pprint(command)
#pprint.pprint(file)

defines.sort()
options.sort()
includes.sort()
unknown.sort()

pprint.pprint(defines)
pprint.pprint(options)
pprint.pprint(includes)
pprint.pprint(unknown)