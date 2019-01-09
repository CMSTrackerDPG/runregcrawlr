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

import re

from runregcrawlr.globalworkspace import GlobalWorkspace
from runregcrawlr.runinfo import RunInfo
from runregcrawlr.tracker import TrackerWorkspace


def crawl_runinfo(*args, **kwargs):
    return RunInfo().get_runs(*args, **kwargs)


def crawl_global(*args, **kwargs):
    return GlobalWorkspace().get_runs(*args, **kwargs)


def crawl_tracker(*args, **kwargs):
    return TrackerWorkspace().get_runs(*args, **kwargs)


def crawl_runs_txt(*args, **kwargs):
    return TrackerWorkspace().get_runs_txt(*args, **kwargs)


def combine_runinfo_global_runs(runinfo_runs, global_runs):
    for run in runinfo_runs:
        run_number = run["run_number"]
        for global_run in list(
            filter(lambda r: r["run_number"] == run_number, global_runs)
        ):
            global_run.update(run)

    _add_reco_and_run_type(global_runs)
    return global_runs


def crawl(*args, **kwargs):
    runinfo_runs = crawl_runinfo(*args, **kwargs)
    global_runs = crawl_global(*args, **kwargs)
    return combine_runinfo_global_runs(runinfo_runs, global_runs)


def _add_reco_and_run_type(global_runs):
    """
    Adds information about the Reconstruction Type and Run Type (Cosmics/Collisions)
    """
    for run in global_runs:
        run["reco"] = (
            re.search(r"^\/[a-zA-Z]*", run["rda_name"]).group(0).replace("/", "")
        )
        run["run_type"] = re.search(r"^[a-zA-Z]*", run["run_class_name"]).group(0)
