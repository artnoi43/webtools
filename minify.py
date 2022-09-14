#!/usr/bin/env python

import os
import sys
import htmlmin

def loop_dir(dir_name, start_path):
    # Save previous CWD before chdir
    prev = os.getcwd()
    os.chdir(dir_name)

    basedir = os.path.basename(".")
    dir_files = os.listdir(basedir)
    for current_file in dir_files:
        if os.path.isdir(current_file):
            prev = f"../{current_file}"
            loop_dir(current_file, start_path)
        if ".html" in current_file:
            read_and_minify(current_file)

    # Try go back to prev.
    # If there's an error, it means that we have traversed most of the subdirs already, so we should go back to .. and see if that is a start_path
    try:
        os.chdir(prev)
    except FileNotFoundError:
      # This error should happen when you are finishing processing newyear.html, assuming that this script processes everything as in the order of the tree below.

#        dist
#        ├── index.html
#        ├── blog
#        │   ├── august.html
#        │   └── newyear.html
#        ├── porn

        if os.path.abspath("..") != start_path:
            os.chdir("..")
        else:
            print("> DONE")
            exit()

visited = {}
def read_and_minify(html_filename):
    fullpath = os.path.abspath(html_filename)
    this_visited = visited.get(fullpath)
    if this_visited:
        return

    fp_r = open(html_filename, "r")
    document = fp_r.read()
    fp_r.close()

    minified = htmlmin.minify(document)
    print(f"> HTML: {html_filename}")
    fp_w = open(html_filename, "w")
    fp_w.write(minified)
    fp_w.close()

    visited[fullpath] = True

if len(sys.argv) < 2:
    print("Missing HTML root directory")
    print("Usage: minify.py <HTML_DIR>")
    exit()

root_dir = sys.argv[1]
print(f'HTML directory: {root_dir}')

path_len = len(root_dir)
trailing = root_dir[path_len-1]
if trailing == "/":
  root_dir = root_dir[:path_len-1]

root_fullpath = os.path.abspath(root_dir)
before_root = os.path.abspath("..")
loop_dir(root_fullpath, before_root)