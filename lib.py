import argparse
import collections
from datetime import datetime
from fnmatch import fnmatch
from math import ceil
import re
import sys
import zlib

import  classes.repo as repo
import  classes.object as object


argparser = argparse.ArgumentParser(description="The stupidest content tracker")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

# INIT
argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")
argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="Where to create the repository.")

# UNHASH
argsp = argsubparsers.add_parser("unhash",help="Provide content of repository objects")
argsp.add_argument("type",
                   metavar="type",
                   choices=["blob", "commit", "tag", "tree"],
                   help="Specify the type")

argsp.add_argument("object",
                   metavar="object",
                   help="The object to display")

# HASH
argsp = argsubparsers.add_parser(
    "hash",
    help="Compute object ID and optionally creates a blob from a file")

argsp.add_argument("-t",
                   metavar="type",
                   dest="type",
                   choices=["blob", "commit", "tag", "tree"],
                   default="blob",
                   help="Specify the type")

argsp.add_argument("-w",
                   dest="write",
                   action="store_true",
                   help="Actually write the object into the database")

argsp.add_argument("path",
                   help="Read object from <file>")




def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "unhash"       : cmd_unhash(args) #git cat-file
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash"         : cmd_hash(args) #git hash_object
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")

def cmd_init(args):
    repo._create(args.path)


def cmd_unhash(args):
    repo_ = repo._find()
    object.cat_file(repo_, args.object, fmt=args.type.encode())

def cmd_hash(args):
    if args.write:
        repo_ = repo._find()
    else:
        repo_ = None

    with open(args.path, "rb") as fd:
        sha = object._hash(fd, args.type.encode(), repo_)
        print(sha)



            



        

  