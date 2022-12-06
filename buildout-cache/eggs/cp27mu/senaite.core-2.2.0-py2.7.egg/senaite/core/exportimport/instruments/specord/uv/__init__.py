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
# Copyright 2018-2020 by it's authors.
# Some rights reserved, see README and LICENSE.

""" Specord
"""
from bika.lims import bikaMessageFactory as _
from bika.lims.utils import t
from senaite.core.exportimport.instruments.resultsimport import \
    InstrumentCSVResultsFileParser, AnalysisResultsImporter
from datetime import datetime

class SpecordCSVParser(InstrumentCSVResultsFileParser):

    def __init__(self, csv, analysiskey):
        InstrumentCSVResultsFileParser.__init__(self, csv)
        self.data_header = None
        self.file_header = {}
        # Set this flag when we find the header-line beginning with "Date,".
        # Once this flag is set, all following lines are real data.
        self.main_data_found = False
        self.analysiskey = analysiskey

    def _parseline(self, line):
        if self.main_data_found:
            this_row = line.split(";")
            # if less values are found than headers, it's an error
            if len(this_row) != len(self.data_header):
                self.err("Data row number  has the wrong number of items")
                return 0
            row_values = dict(zip(self.data_header, this_row))

            raw_result = {}
            for d in (row_values, self.file_header):
                raw_result.update(d)
            raw_result['DefaultResult'] = 'LEC'
            raw_result = {self.analysiskey: raw_result};

            sample_id = row_values['Nombre']
            self._addRawResult(sample_id, raw_result)

        elif line.startswith('Nombre'):
            line = line.replace('Conc. [mg/l]', 'LEC')
            line = line.replace('Divisor 2;', 'Divisor 2')
            self.data_header = line.split(';')
            self.main_data_found = True

        return 0

class SpecordImporter(AnalysisResultsImporter):

    def __init__(self, parser, context,  override,
                 allowed_ar_states=None, allowed_analysis_states=None,
                 instrument_uid=None):
        AnalysisResultsImporter.__init__(self, parser, context,
                                          override,
                                         allowed_ar_states,
                                         allowed_analysis_states,
                                         instrument_uid)
