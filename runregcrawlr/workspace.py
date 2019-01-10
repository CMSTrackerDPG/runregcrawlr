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
    ):

        table = "datasets"
        query = (
            "select {fields} "
            "from {namespace}.{table} {table_alias} "
            "where {run_where}{additional_where} "
            "order by {table_alias}.run_number".format(
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
        column_names = self.get_column_names(table)
        data = response.get("data", None)
        return list_to_dict(data, column_names)
