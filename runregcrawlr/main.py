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

from runregcrawlr.crawler import (
    crawl,
    crawl_runinfo,
    crawl_global,
    crawl_runs_txt,
    crawl_tracker,
    crawl_tracker_lumis,
)

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

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--runinfo-workspace", help="Use only RunInfo workspace", action="store_true"
    )

    group.add_argument(
        "--global-workspace", help="Use only Global workspace.", action="store_true"
    )

    group.add_argument(
        "--tracker",
        help="Use only Tracker workspace (Express and Prompt).",
        action="store_true",
    )

    group.add_argument(
        "--tracker-lumis",
        help="Use Tracker workspace (Express and Prompt) with Lumis.",
        action="store_true",
    )

    group.add_argument(
        "--runs-txt",
        help="Generate a runs.txt file containg runnumber and reconstruction.",
        action="store_true",
    )

    return parser.parse_args()


def save_to_disk(content, filename=OUTPUT_FILE_NAME):
    with open(filename, "w") as file:
        file.write(content)


def _determine_crawl_function(args):
    """
    Analyzes command line arguments and returns corresponding crawling function
    """
    if args.runinfo_workspace:
        return crawl_runinfo
    if args.global_workspace:
        return crawl_global
    if args.tracker:
        return crawl_tracker
    if args.tracker_lumis:
        return crawl_tracker_lumis
    if args.runs_txt:
        return crawl_runs_txt
    return crawl


def _create_runs_txt_content(runs):
    content = ""
    for run in runs:
        if "cosmic" not in run[2].lower() and "commissioning" not in run[2].lower():
            content += "{} {} {}\n".format(run[0], run[1], run[2])
    return content


def main():
    args = parse_arguments()

    if args.run or args.min or args.max or args.list:
        crawl_function = _determine_crawl_function(args)
        runs = crawl_function(
            run_number=args.run,
            run_number_from=args.min,
            run_number_to=args.max,
            run_number_in=args.list,
        )
        if args.runs_txt:
            filename = "runs.txt"
            content = _create_runs_txt_content(runs)
            num = content.count("\n")
        else:
            filename = OUTPUT_FILE_NAME
            content = simplejson.dumps(runs, indent=2)
            num = len(runs)

        save_to_disk(content, filename)
        print("Stored {} entries in file '{}'".format(num, filename))
    else:
        print("Please use at least one run number argument")


if __name__ == "__main__":
    main()
