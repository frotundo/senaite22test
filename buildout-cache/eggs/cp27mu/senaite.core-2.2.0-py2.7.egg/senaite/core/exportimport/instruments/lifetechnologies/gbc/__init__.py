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

""" GBC
"""
from bika.lims import bikaMessageFactory as _
from bika.lims.utils import t
from senaite.core.exportimport.instruments.resultsimport import \
    InstrumentCSVResultsFileParser, AnalysisResultsImporter
from datetime import datetime

import re


class GbcCSVParser(InstrumentCSVResultsFileParser):

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
            this_row = line.split("\t")
            # if less values are found than headers, it's an error
            if len(this_row) != len(self.data_header):
                self.err("Data row number  has the wrong number of items")
                return 0

            row_values = dict(zip(self.data_header, this_row))

            raw_result = {}
            for d in (row_values, self.file_header):
                raw_result.update(d)

            #raw_result['DefaultResult'] = 'LEC'
            # raw_result = {self.analysiskey: raw_result}
            sample_id = row_values['Muestra Etiqueta']
            # self._addRawResult(sample_id, raw_result)
            #if self.analysiskey.find("LEC") or self.analysiskey.find("ABS"):
            if float(row_values['ABS']) <= 0.0044:
                row_values['LEC'] = '0.0'
            # self._addRawResult(sample_id,self.analysiskey ,'LEC',0, 'ABS',1)
                self._addRawResult(sample_id, values={self.analysiskey: row_values})
            else:
                    # raw_result = self.data_header['LEC'], 0
                self._addRawResult(sample_id, values={self.analysiskey: raw_result})
            #else:
            #    self._addRawResult(sample_id, values={self.analysiskey: raw_result}, override=False)


        elif line.startswith('Muestra Etiqueta'):
            line = line.replace(chr(181), 'u')
            line = line.replace('Conc. (ug/ml)', 'LEC')
            line = line.replace('Media Abs.', 'ABS')
            self.data_header = line.split('\t')
            self.main_data_found = True

        # elif not line.startswith(',,'):
        # Header
        # splitted = line.split("\t")
        # if len(splitted) > 0:
        #    name = splitted[0].strip()
        #    val = splitted[1].strip() if len(splitted) > 1 else ''
        #    self.file_header[name] = val

        return 0


class GbcImporter(AnalysisResultsImporter):

    def __init__(self, parser, context, override,
                 allowed_ar_states=None, allowed_analysis_states=None,
                 instrument_uid=None):
        AnalysisResultsImporter.__init__(self, parser, context, override,
                                         allowed_ar_states,
                                         allowed_analysis_states,
                                         instrument_uid)