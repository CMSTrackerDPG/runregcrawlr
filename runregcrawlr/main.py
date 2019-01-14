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

from runregcrawlr.crawler import get_runs_txt_data, get_data
from runregcrawlr.globalworkspace import GlobalWorkspace
from runregcrawlr.tracker import TrackerWorkspace


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CMS Run Registry crawler.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=36),
    )

    parser.add_argument("--min", help="Minimum run number")
    parser.add_argument("--max", help="Maximum run number")
    parser.add_argument("--run", help="Single run number")
    parser.add_argument("--list", nargs="*", help="Multiple run numbers")
    parser.add_argument("--workspace", choices=["global", "tracker"], default="global")
    parser.add_argument("--out", help="Output file name")

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--add-lumis",
        help="Add lumisection and luminosity information.",
        action="store_true",
    )

    group.add_argument(
        "--runs-txt",
        help="Generate a runs.txt file containing run number and reconstruction.",
        action="store_true",
    )

    parser.add_argument(
        "--exclude-non-regular",
        help="Exclude commissioning and special runs",
        action="store_true",
    )

    parser.add_argument(
        "--exclude-cosmics", help="Exclude cosmics runs", action="store_true"
    )

    return parser.parse_args()


def save_to_disk(content, filename):
    with open(filename, "w") as file:
        file.write(content)


def _determine_workspace(args):
    workspace = args.workspace

    if workspace == "tracker":
        print("Using Tracker workspace")
        return TrackerWorkspace
    if workspace == "global":
        print("Using Global workspace")
        return GlobalWorkspace
    raise Exception("Unkown workspace '{}'".format(workspace))


def _create_runs_txt_content(runs):
    content = ""
    for run in runs:
        # if "cosmic" not in run[2].lower() and "commissioning" not in run[2].lower():
        content += "{} {} {}\n".format(run[0], run[1], run[2])
    return content


def main():
    args = parse_arguments()

    if not args.run and not args.min and not args.max and not args.list:
        print("Please use at least one run number argument")
        return

    kwargs = {
        "run_number": args.run,
        "run_number_from": args.min,
        "run_number_to": args.max,
        "run_number_in": args.list,
    }

    if args.add_lumis:
        kwargs["add_lumis"] = True

    if args.exclude_non_regular:
        kwargs["exclude_non_regular"] = True

    if args.exclude_cosmics:
        kwargs["exclude_cosmics"] = True

    workspace = _determine_workspace(args)

    if args.runs_txt:
        filename = "runs.txt"
        runs = get_runs_txt_data(workspace, **kwargs)
        content = _create_runs_txt_content(runs)
        num = content.count("\n")
    else:
        filename = "runregcrawlr-{}-output.json".format(args.workspace)
        runs = get_data(workspace, **kwargs)
        content = simplejson.dumps(runs, indent=2)
        num = len(runs)

    filename = args.out if args.out else filename
    save_to_disk(content, filename)
    print("Stored {} entries in file '{}'".format(num, filename))


if __name__ == "__main__":
    main()
