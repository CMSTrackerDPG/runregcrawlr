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
from .utils import build_where_clause, list_to_dict


class GlobalWorkspace(RunRegistryWorkspace):
    def __init__(self):
        super(GlobalWorkspace, self).__init__("runreg_global")

    def get_runs(
        self,
        run_number=None,
        run_number_from=None,
        run_number_to=None,
        run_number_in=None,
        exclude_online=False,
    ):
        """
        Note: Express runs are not in the global workspace

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
