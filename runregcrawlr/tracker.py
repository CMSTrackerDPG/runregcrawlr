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

from .client import RunRegistryClient
from .utils import build_where_clause, list_to_dict


class TrackerWorkspace:
    def __init__(self):
        self.runregistry = RunRegistryClient()
        self.namespace = "runreg_tracker"
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

    def get_runs(
        self,
        run_number=None,
        run_number_from=None,
        run_number_to=None,
        run_number_in=None,
        exclude_online=False,
    ):
        """
        :param run_number:
        :param run_number_from:
        :param run_number_to:
        :param run_number_in:
        :return:
        """
        table = "datasets"
        query = (
            "select "
            "* "
            "from {namespace}.{table} r where {run_where}".format(
                namespace=self.namespace,
                table=table,
                run_where=build_where_clause(
                    "r.run_number",
                    run_number,
                    run_number_from,
                    run_number_to,
                    run_number_in,
                ),
            )
        )

        if exclude_online:
            query += " and r.rda_name != '/Global/Online/ALL'"

        response = self.runregistry.execute_query(query, inline_clob=True)
        column_names = self.get_column_names(table)
        return list_to_dict(response.get("data", None), column_names)

    def get_runs_txt(
        self,
        run_number=None,
        run_number_from=None,
        run_number_to=None,
        run_number_in=None,
    ):
        """
        Returns run number, reconstruction type and run class
        """
        table = "datasets"
        query = (
            "select "
            "r.run_number, r.rda_name, r.run_class_name "
            "from {namespace}.{table} r where {run_where}".format(
                namespace=self.namespace,
                table=table,
                run_where=build_where_clause(
                    "r.run_number",
                    run_number,
                    run_number_from,
                    run_number_to,
                    run_number_in,
                ),
            )
        )

        query += " order by r.run_number"

        response = self.runregistry.execute_query(query, inline_clob=True)
        runs = response.get("data")
        for run in runs:
            run[1] = re.search(r"^\/[a-zA-Z]*", run[1]).group(0).replace("/", "")
            if run[1] == "Global":
                run[1] = "Online"
            if run[1] == "PromptReco":
                run[1] = "Prompt"
            run[2] = re.search(r"^[a-zA-Z]*", run[2]).group(0)

        return runs
