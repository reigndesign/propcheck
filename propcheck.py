#!/usr/bin/python
import fnmatch
import os
import re
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--strict", help="strict mode", action="store_true")
parser.add_argument("--path", help="strict mode")
args = parser.parse_args()

strict = args.strict
if args.path:
    path = args.path
else:
    path = "."

files = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(path)
    for f in fnmatch.filter(files, '*.h')+fnmatch.filter(files, '*.m')]
    


def check(line,file,lineno):
    
    accessors = re.search(r"\(([^)]*)\)",line)
    if not accessors:
        print "%s:%s:%s has no accessors" % (file, str(lineno), line)
        return
    accessors_list = [a.strip() for a in accessors.group(1).split(",")]
    
    is_outlet_collection = "IBOutletCollection" in line
    is_outlet = "IBOutlet" in line and not is_outlet_collection
    is_delegate = "delegate" in line.lower()
    is_string = "NSString" in line
    is_block = "(^" in line
    is_pointer = "*" in line and not is_block
    
    
    
    #pointers should be strong, unless they are outlets or strings
    if strict and is_pointer and not is_outlet and not is_string and "strong" not in accessors_list: 
        print "%s:%s:%s should probably be strong" % (file, str(lineno), line)
             
    #strings should be copy
    if is_pointer and is_string and "copy" not in accessors_list: 
        print "%s:%s:%s should probably be copy" % (file, str(lineno), line)
    
    #outlets should be weak    
    if is_pointer and is_outlet and "weak" not in accessors_list: 
        print "%s:%s:%s should probably be weak" % (file, str(lineno), line)
        
    #delegates should be weak    
    if is_delegate and "weak" not in accessors_list: 
        print "%s:%s:%s should probably be weak" % (file, str(lineno), line)

    #primitives should be assign
    if strict and not is_pointer and not is_delegate and not is_block and "assign" not in accessors_list:
        print "%s:%s:%s should probably be assign" % (file, str(lineno), line)

    #blocks should be copy
    if is_block and "copy" not in accessors_list: 
        print "%s:%s:%s should probably be copy" % (file, str(lineno), line)
    

    #everything should be nonatomic
    if "nonatomic" not in accessors_list:
        print "%s:%s:%s should probably be nonatomic" % (file, str(lineno), line)
             

for file in files:
    f = open(file)
    data = f.read()
    f.close()
    lines = data.split("\n")
    for (i,line) in enumerate(lines):
        if line.strip().startswith("@property"):
            check(line,file,i+1)