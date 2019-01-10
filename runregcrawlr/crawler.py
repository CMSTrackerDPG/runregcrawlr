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

from runregcrawlr.runinfo import RunInfo


def get_runs_txt_data(WorkspaceClass, *args, **kwargs):
    return WorkspaceClass().get_runs_txt(*args, **kwargs)


def get_data(WorkspaceClass, add_lumis=False, *args, **kwargs):
    data = WorkspaceClass().get_runs(*args, **kwargs)
    if add_lumis:
        lumis = RunInfo().get_runs(*args, **kwargs)
        data = _combine(lumis, data)
    return data


def _combine(runinfo_runs, dataset_runs):
    for run in runinfo_runs:
        run_number = run["run_number"]
        for dataset_run in list(
            filter(lambda r: r["run_number"] == run_number, dataset_runs)
        ):
            dataset_run.update(run)

    _add_reco_and_run_type(dataset_runs)
    return dataset_runs


def _add_reco_and_run_type(global_runs):
    """
    Adds information about the Reconstruction Type and Run Type (Cosmics/Collisions)
    """
    for run in global_runs:
        run["reco"] = (
            re.search(r"^\/[a-zA-Z]*", run["rda_name"]).group(0).replace("/", "")
        )
        run["run_type"] = re.search(r"^[a-zA-Z]*", run["run_class_name"]).group(0)
