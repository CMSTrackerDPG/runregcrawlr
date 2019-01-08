#!/usr/bin/python
# -*- coding: utf-8 -*-

# © Copyright 2018 CERN
#
# This software is distributed under the terms of the GNU Lesser General Public
# Licence version 3 (LGPL Version 3), copied verbatim in the file “LICENSE”
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

import argparse
import simplejson

from runregcrawlr.crawler import crawl

OUTPUT_FILE_NAME = "runregcrawlr-output.json"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CMS Run Registry crawler.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=36),
    )

    parser.add_argument("--min", help="Minimum run number")
    parser.add_argument("--max", help="Maximum run number")
    parser.add_argument("--run", help="Single run number")
    parser.add_argument("--list", nargs="*", help="Multiple run numbers")

    return parser.parse_args()


def save_to_disk(content):
    with open(OUTPUT_FILE_NAME, "w") as file:
        file.write(content)


def main():
    args = parse_arguments()

    if args.run or args.min or args.max or args.list:
        runs = crawl(
            run_number=args.run,
            run_number_from=args.min,
            run_number_to=args.max,
            run_number_in=args.list,
        )
        save_to_disk(simplejson.dumps(runs, indent=2))
        print("Stored {} entries in file '{}'".format(len(runs), OUTPUT_FILE_NAME))
    else:
        print("Please use at least one argument")


if __name__ == "__main__":
    main()
