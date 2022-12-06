# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2019 by it's authors.
# Some rights reserved, see README and LICENSE.

""" Perkin ELMER-PRO ICP
"""
from bika.lims import api
from datetime import datetime
from bika.lims.catalog import CATALOG_ANALYSIS_REQUEST_LISTING
from bika.lims.browser import BrowserView
from senaite.core.exportimport.instruments.resultsimport import \
    AnalysisResultsImporter, InstrumentCSVResultsFileParser

import json
import re
import traceback


def is_keyword(kw):
    bsc = api.get_tool('bika_setup_catalog')
    return len(bsc(getKeyword=kw))


def find_analyses(ar_or_sample):
    """ This function is used to find keywords that are not on the analysis
        but keywords that are on the interim fields.

        This function and is is_keyword function should probably be in
        resultsimport.py or somewhere central where it can be used by other
        instrument interfaces.
    """
    bc = api.get_tool(CATALOG_ANALYSIS_REQUEST_LISTING)
    ar = bc(portal_type='AnalysisRequest', id=ar_or_sample)
    if len(ar) == 0:
        ar = bc(portal_type='AnalysisRequest', getClientSampleID=ar_or_sample)
    if len(ar) == 1:
        obj = ar[0].getObject()
        analyses = obj.getAnalyses(full_objects=True)
        return analyses
    return []


def get_interims_keywords(analysis):
    interims = api.safe_getattr(analysis, 'getInterimFields')
    return map(lambda item: item['keyword'], interims)



def find_kw(ar_or_sample, kw):
    """ This function is used to find keywords that are not on the analysis
        but keywords that are on the interim fields.

        This function and is is_keyword function should probably be in
        resultsimport.py or somewhere central where it can be used by other
        instrument interfaces.
    """
    for analysis in find_analyses(ar_or_sample):
        if kw in get_interims_keywords(analysis):
            return analysis.getKeyword()
    return None

class PerkinelmerSyngistixCSV2Parser(InstrumentCSVResultsFileParser):
    def __init__(self, csv):
        InstrumentCSVResultsFileParser.__init__(self, csv)
        self._columns = []  # The different columns names
        self._values = {}  # The analysis services from the same resid
        self._resid = ''  # A stored resid
        self._rownum = None
        self._end_header = False


    def _parseline(self, line):
        sline = line.split(';')
        if len(sline) > 0 and not self._end_header:
            self._columns = sline
            self._end_header = True
            return 0
        elif sline > 0 and self._end_header:
            self.parse_data_line(sline)
        else:
            self.err("Unexpected data format", numline=self._numline)
            return -1

    def parse_data_line(self, sline):
        """
        Parses the data line and builds the dictionary.
        :param sline: a split data line to parse
        :returns: the number of rows to jump and parse the next data line or return the code error -1
        """
        # if there are less values founded than headers, it's an error
        found = False
        if len(sline) != len(self._columns):
            self.err("One data line has the wrong number of items")
            return -1
        rawdict = {}
        for idx, result in enumerate(sline):
            rawdict[self._columns[idx]] = result
        # Getting key values
        resid = rawdict['Sample ID']
        del rawdict['Sample ID']
        if resid[-1] == 'D':
            resid = resid.replace("D", "")
            kw = rawdict['Elem']
            kw = kw+"D"
        else:
            resid = resid
            kw = rawdict['Elem']

        # Building the new dict
        rawdict['DefaultResult'] = rawdict['Reported Conc (Samp)']
        del rawdict['Reported Conc (Samp)']
        rawdict['Remarks'] = rawdict['Analyte Name']
        del rawdict['Analyte Name']
        if not is_keyword(kw):
            new_kw = find_kw(resid, kw)
            if new_kw:
                found = True
            if found:
                rawdict[kw] = rawdict['DefaultResult']
                del rawdict['DefaultResult']

                kw = new_kw
                kw = re.sub(r"\W", "", kw)

        self._addRawResult(resid,
                          values={kw: rawdict},
                          override=False)
        return 0

    found = False


class PerkinelmerSyngistix2Importer(AnalysisResultsImporter):
    def __init__(self, parser, context,  override,
                 allowed_ar_states=None, allowed_analysis_states=None,
                 instrument_uid=None):
        AnalysisResultsImporter.__init__(self, parser, context,
                                          override,
                                         allowed_ar_states,
                                         allowed_analysis_states,
                                         instrument_uid)
