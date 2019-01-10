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

from .workspace import RunRegistryWorkspace


class GlobalWorkspace(RunRegistryWorkspace):
    def __init__(self):
        super(GlobalWorkspace, self).__init__("runreg_global")

    def get_runs(self, **kwargs):
        return self.get_dataset_runs(**kwargs)
