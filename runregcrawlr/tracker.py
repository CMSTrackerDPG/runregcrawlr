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

from .workspace import RunRegistryWorkspace


class TrackerWorkspace(RunRegistryWorkspace):
    def __init__(self):
        super(TrackerWorkspace, self).__init__("runreg_tracker")

    def get_runs(self, **kwargs):
        return self.get_dataset_runs(**kwargs)

    def get_non_regular_run_numbers(self, **kwargs):
        where = "(r.rda_name like '%ecial%' or r.rda_name like '%ommiss%')"
        return self.get_dataset_runs(where=where, **kwargs)

    def get_runs_txt(self, **kwargs):
        """
        Returns run number, reconstruction type and run class
        """
        fields = "r.run_number, r.rda_name, r.run_class_name"
        runs = self.get_dataset_runs(fields=fields, **kwargs)
        for run in runs:
            run[1] = re.search(r"^\/[a-zA-Z]*", run[1]).group(0).replace("/", "")
            if run[1] == "Global":
                run[1] = "Online"
            if run[1] == "PromptReco":
                run[1] = "Prompt"
            run[2] = re.search(r"^[a-zA-Z]*", run[2]).group(0)

        return runs
