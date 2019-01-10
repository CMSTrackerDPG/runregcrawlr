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

from .client import RunRegistryClient


class RunRegistryWorkspace:
    def __init__(self, namespace):
        self.runregistry = RunRegistryClient()
        self.namespace = namespace
        self.column_names = {}

    def get_column_names(self, table):
        if table not in self.column_names:
            table_description = self.runregistry.get_table_description(
                self.namespace, table
            )
            self.column_names[table] = [
                column["name"].lower() for column in table_description["columns"]
            ]
        return self.column_names[table]
