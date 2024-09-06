import argparse
from datetime import datetime
from fnmatch import fnmatch
from math import ceil
import re
import os
import sys
import zlib

import  classes.repo as repo
import  classes.object as object
import  classes.commit as commit
import  classes.tree as tree

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

# LOG

argsp = argsubparsers.add_parser("log", help="Display history of a given commit.")
argsp.add_argument("commit",
                   default="HEAD",
                   nargs="?",
                   help="Commit to start at.")

# LS-TREE

argsp = argsubparsers.add_parser("ls-tree", help="Pretty-print a tree object.")
argsp.add_argument("-r",
                   dest="recursive",
                   action="store_true",
                   help="Recurse into sub-trees")

argsp.add_argument("tree",
                   help="A tree-ish object.")

# CHECKOUT

argsp = argsubparsers.add_parser("checkout", help="Checkout a commit inside of a directory.")

argsp.add_argument("commit",
                   help="The commit or tree to checkout.")

argsp.add_argument("path",
                   help="The EMPTY directory to checkout on.")

# SHOW-REF
argsp = argsubparsers.add_parser("show-ref", help="List references.")

def main(argv=sys.argv[1:]):
    if len(argv) == 0:
        return argparser.print_usage();

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

def cmd_log(args):
    repo_ = repo._find()

    print("digraph wyaglog{")
    print("  node[shape=rect]")
    object.log(repo_, object._find(repo_, args.commit), set())
    print("}")



def cmd_ls_tree(args):
    repo_ = repo._find()
    object.ls_tree(repo_, args.tree, args.recursive)

def cmd_checkout(args):
    repo_ = repo._find()

    obj = object._read(repo_, object._find(repo_, args.commit))

    # If the object is a commit, we grab its tree
    if obj.fmt == b'commit':
        obj = object._read(repo_, obj.kvlm[b'tree'].decode("ascii"))

    # Verify that path is an empty directory
    if os.path.exists(args.path):
        if not os.path.isdir(args.path):
            raise Exception("Not a directory {0}!".format(args.path))
        if os.listdir(args.path):
            raise Exception("Not empty {0}!".format(args.path))
    else:
        os.makedirs(args.path)

    object.checkout(repo_, obj, os.path.realpath(args.path))
            


def cmd_show_ref(args):
    repo_ = repo._find()
    refs = object.ref_list(repo_)
    object.show_ref(repo_, refs, prefix="refs")

        

  