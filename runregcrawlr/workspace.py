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

from .utils import list_to_dict, build_where_clause
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

    def get_dataset_runs(
        self,
        where=None,
        fields="*",
        run_number=None,
        run_number_from=None,
        run_number_to=None,
        run_number_in=None,
        table_alias="r",
        flat=False,
    ):

        table = "datasets"
        query = (
            "select {fields} "
            "from {namespace}.{table} {table_alias} "
            "where {run_where}{additional_where} "
            "order by {table_alias}.run_number, {table_alias}.rda_name".format(
                fields=fields,
                namespace=self.namespace,
                table=table,
                run_where=build_where_clause(
                    "{table_alias}.run_number".format(table_alias=table_alias),
                    run_number,
                    run_number_from,
                    run_number_to,
                    run_number_in,
                ),
                table_alias=table_alias,
                additional_where=" and {where}".format(where=where) if where else "",
            )
        )

        response = self.runregistry.execute_query(query, inline_clob=True)
        data = response.get("data", None)

        if flat:
            return data

        if fields == "*":
            column_names = self.get_column_names(table)
        else:
            column_names = (
                fields.replace(" ", "")
                .replace("{}.".format(table_alias), "")
                .split(",")
            )
        return list_to_dict(data, column_names)

    def get_runs(self, **kwargs):
        return self.get_dataset_runs(**kwargs)

    def get_non_regular_run_numbers(self, **kwargs):
        where = "(r.rda_name like '%ecial%' or r.rda_name like '%ommiss%')"
        runs = self.get_dataset_runs(where=where, **kwargs)
        return sorted({run["run_number"] for run in runs})

    def get_runs_txt(self, **kwargs):
        """
        Returns run number, reconstruction type and run class
        """
        fields = "r.run_number, r.rda_name, r.run_class_name"
        runs = self.get_dataset_runs(fields=fields, flat=True, **kwargs)
        for run in runs:
            run[1] = re.search(r"^\/[a-zA-Z]*", run[1]).group(0).replace("/", "")
            if run[1] == "Global":
                run[1] = "Online"
            if run[1] == "PromptReco":
                run[1] = "Prompt"
            run[2] = re.search(r"^[a-zA-Z]*", run[2]).group(0)
        return runs
