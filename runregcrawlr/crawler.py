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


def get_runs_txt_data(
    workspace_class, exclude_non_regular=False, exclude_cosmics=False, *args, **kwargs
):
    workspace = workspace_class()
    runs = workspace.get_runs_txt(*args, **kwargs)

    if exclude_non_regular:
        non_regular_runs = workspace.get_non_regular_run_numbers(*args, **kwargs)
        runs = list(filter(lambda run: run[0] not in non_regular_runs, runs))

    if exclude_cosmics:
        cosmics_runs = workspace.get_cosmics_run_numbers(*args, **kwargs)
        runs = list(filter(lambda run: run[0] not in cosmics_runs, runs))

    return runs


def get_data(
    workspace_class,
    add_lumis=False,
    exclude_non_regular=False,
    exclude_cosmics=False,
    *args,
    **kwargs
):
    workspace = workspace_class()
    data = workspace.get_runs(*args, **kwargs)

    if add_lumis:
        lumis = RunInfo().get_runs(*args, **kwargs)
        data = _combine(lumis, data)

    if exclude_non_regular:
        non_regular_runs = workspace.get_non_regular_run_numbers(*args, **kwargs)
        data = list(filter(lambda run: run["run_number"] not in non_regular_runs, data))

    if exclude_cosmics:
        cosmics_runs = workspace.get_cosmics_run_numbers(*args, **kwargs)
        data = list(filter(lambda run: run["run_number"] not in cosmics_runs, data))

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
