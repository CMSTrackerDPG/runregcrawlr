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


def list_as_comma_separated_string(items):
    """
    Converts a list of items into a single comma separated string
    of single quoted items

    :param items: list of items
    :return: comma separated string of quoted items
    """
    return ", ".join(["'" + str(item) + "'" for item in items])


def list_to_dict(list_of_lists, keys):
    """
    Turns a list of lists into a list of dictionaries

    :param list_of_lists: list of lists
    :param keys: keys for the dictionary
    :return: list of dictionaries
    """
    return [dict(zip(keys, item)) for item in list_of_lists]


def build_where_clause(
    attribute, value=None, value_from=None, value_to=None, value_in=None
):
    """
    :param attribute: name of the attribute e.g. r.runnumber
    :param value_from: value has to be at least
    :param value_to: value cant be higher than
    :param value_in: value is in list e.g. [333444, 333456]
    :return:
    """
    items = []

    if value:
        items.append("{} = '{}'".format(attribute, value))
    if value_from:
        items.append("{} >= '{}'".format(attribute, value_from))
    if value_to:
        items.append("{} <= '{}'".format(attribute, value_to))
    if value_in:
        items.append(
            "{} in ({})".format(attribute, list_as_comma_separated_string(value_in))
        )

    return " and ".join(items) if items else "1 = 1"
