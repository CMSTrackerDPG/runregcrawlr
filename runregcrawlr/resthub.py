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

import logging
from json import JSONDecodeError
from math import ceil

import requests

from .singleton import Singleton

logger = logging.getLogger(__name__)


class RestHubClient():
    """
    Implements a simple client that accesses a RestHub API

    See:
    https://github.com/valdasraps/RestHub
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/DqmRrApi
    """

    def __init__(self, url):
        self.url = url
        self._connection_successful = None  # Lazy
        self.row_limit = 1000

    def _test_connection(self):
        try:
            requests.get(self.url)
            return True
        except requests.ConnectionError:
            return False

    def retry_connection(self):
        """
        Retry to connect to RestHub API.
        Updates return value of the connection_possible method.
        """
        self._connection_successful = self._test_connection()

    def connection_possible(self):
        """
        Check if the connection to the RestHub API is possible.

        :return: True when connection to Run Registry was successful
        """
        if self._connection_successful is None:
            self.retry_connection()
        return self._connection_successful

    def _get_count(self, query_id):
        """
        :param query_id: query id
        :return: amount of rows that the query_id contains
        """
        if not self.connection_possible():
            logger.error("Connection to {} not possible".format(self.url))
            return 0
        count = requests.get("{}/query/{}/count".format(self.url, query_id)).json()
        return count

    def _get_json_response(self, resource, media_type=None, inline_clob=False):
        if not self.connection_possible():
            logger.error("Connection to {} not possible".format(self.url))
            return {}

        params = {"_inclob": "True"} if inline_clob else None
        headers = {"Accept": media_type} if media_type else None

        try:
            response = requests.get(self.url + resource, headers=headers, params=params)
            if media_type:
                return response.content.decode("utf-8")
            return response.json()
        except ValueError as e:
            logger.error(e)
            return {}

    def _get_paged_json_response(self, query_id, inline_clob=False):
        """
        Retrieves the response page-wise.

        Necessary when the response has more than 1000 rows.
        """
        count = self._get_count(query_id)
        number_of_pages = int(ceil(count / self.row_limit))
        entries = {"data": []}

        for page in range(0, number_of_pages):
            resource = "/query/{}/page/{}/{}/data".format(
                query_id, self.row_limit, page + 1
            )
            response = self._get_json_response(resource, inline_clob)
            entries["data"].extend(response["data"])

        return entries

    def _get_query_id(self, query):
        """
        Converts a SQL query string into a query id (qid), that will be used to access
        the RestHub API.

        POST: /query

        :param query: SQL query string
        :return: query id
        """
        response = requests.post(self.url + "/query?", data=query)
        if response.status_code == 400:
            raise ValueError(response.text)
        response.raise_for_status()
        return response.text

    def execute_query(self, query, media_type=None, inline_clob=False):
        """
        Executes an arbitrary SQL query

        GET: /query/{query_id}

        Limitations:
         - tables referred by namespace.table
         - all tables used must have the unique alias in a query
         - only tables that share the same connection can be used in a query
         - named parameters are supported, i.e. :name
         - by default named parameter is considered of string type
         - named parameter type can be changed with prefix:
           - s__{parameter name} string type, i.e. s__name, s__country
           - n__{parameter name} number type, i.e. n__id, n__voltage
           - d__{parameter name} date type, i.e. d__from, d__to
         - supported functions can be found under /info

        :param media_type: Desired media type, e.g. application/xml, text/json
        :param query: SQL query string
        :return: JSON dictionary
        """
        if not self.connection_possible():
            logger.error("Connection to {} not possible".format(self.url))
            return {}
        query_id = self._get_query_id(query)
        count = self._get_count(query_id)
        if count > self.row_limit:
            return self._get_paged_json_response(query_id, inline_clob)
        else:
            resource = "/query/" + query_id + "/data"
            return self._get_json_response(resource, media_type, inline_clob)

    def get_table_description(self, namespace, table):
        """
        Table description in JSON

        :param namespace: runreg_{workspace}, e.g. runreg_tracker
        :param table: runs, run_lumis, datasets, dataset_lumis
        :return: json containing the table description
        """
        resource = "/table/{}/{}".format(namespace, table)
        return self._get_json_response(resource)

    def get_queries(self):
        """
        GET /queries/

        :return: list of queries
        """
        return self._get_json_response("/queries")

    def get_query_description(self, query_id):
        """
        GET /query/{query_id}

        :return: json dictionary with query description
        """
        return self._get_json_response("/query/{}".format(query_id))

    def get_info(self):
        """
        GET /info

        Contains a list of supported functions and the version numbers.

        :return json with general information about the service
        """
        return self._get_json_response("/info")
