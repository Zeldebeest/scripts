'''
Created on 5 Dec 2012

@author: linc2027
'''

import os
import numpy as np
from StringIO import StringIO
import re

class Probe:
    """ Holds all the stuff parsed from a log file:
    # totalAv_I: average intensity over whole dataset.
    # overall_summary, inner_shell_summary, and outer_shell_summary:
    #     the summary (table 1) data for this log filew
    # wilsonB: the wilson B factor for this log file.
    # probe_number: the dataset number for this wedge."""

    def __init__(self, name):
        self.tad95 = None
        self.dwd = None
        self.ad_wc = None
        self.maxDose = float
        self.name = name
        self.probe_number = None
        self.wilsonB = None
        self.overall_summary = []
        self.inner_shell_summary = []
        self.outer_shell_summary = []
        self.totalAv_I = None
        self.av_I_data = [['Res bin', 'Bin Limit', 'Av_I', 'Mn(I/sd)']]
        summary_fields = ['Low resolution limit',
                          'High resolution limit',
                          'Rmerge',
                          'Rmerge in top intensity bin',
                          'Rmeas (within I+/I-)',
                          'Rmeas (all I+ & I-) ',
                          'Rpim (within I+/I-)',
                          'Rpim (all I+ & I-)',
                          'Fractional partial bias',
                          'Total number of observations',
                          'Total number unique',
                          'Mean((I)/sd(I))',
                          'Completeness',
                          'Multiplicity',
                          'Anomalous completeness',
                          'Anomalous multiplicity',
                          'DelAnom correlation between half-sets',
                          'Mid-Slope of Anom Normal Probability']


def processFolderWithACrystal(folder, crystalID):

    logFiles = os.listdir(folder)
    crystalID_regex = re.compile('\(IDENT\):\sprobe([0-9]{1,2})')
    scalaNumbers_regex = re.compile("\s+((-?[0-9]+(\.[0-9]+)?)|-)"
                              "\s+((-?[0-9]+(\.[0-9]+)?)|-)"
                              "\s+((-?[0-9]+(\.[0-9]+)?)|-)$")
    # outputCSVName_regex = re.compile(r'output-SummaryCSV(\([0-9]+\))?')
    crystal = {}

    for current_log_file in logFiles:
        if ".csv" in current_log_file:
            with open(folder + '\\' + current_log_file, 'r') as dose_array:
                dose_data = np.genfromtxt(dose_array,
                                          dtype=float,
                                          delimiter=',',
                                          skip_header=1,
                                          usecols={0, 1, 2, 6, 7},
                                          names={'Wedge number',
                                                 'Diffracted Dose',
                                                 'AD-WC',
                                                 'TAD-95',
                                                 'Max Dose'},
                                          )

    for current_log_file in logFiles:
        if '.log' in current_log_file:
            in_dollar_block = False
            in_av_I_block = False
            in_sum_data_block = False
            in_table_1 = False

            thisProbe = Probe(current_log_file)

            with open(folder + '\\' + current_log_file, 'r') as current_log:
                for line in current_log:

                    # Find crystal IDENT -  from MOSFLM
                    if 'Crystal identifier (IDENT):' in line:
                        crystalID_reg = crystalID_regex.search(line)
                        thisProbe.probe_number = int(crystalID_reg.group(1))

                    # Start of section containing average I from SCALA
                    if '4SINTH' in line:
                        in_av_I_block = True
                    if in_av_I_block:
                        if in_dollar_block:
                            if line.startswith(' $$'):
                                in_dollar_block = False
                            else:
                                this_line = StringIO(line)
                                numpy_line = np.genfromtxt(this_line,
                                                           usecols=(0,
                                                                    2,
                                                                    8,
                                                                    12)
                                                           )
                                thisProbe.av_I_data.append([numpy_line[0],
                                                            numpy_line[1],
                                                            numpy_line[2],
                                                            numpy_line[3]])
                        else:
                            if line.startswith(' $$'):
                                in_dollar_block = True
                        if line.startswith(' Overall'):
                            this_line = StringIO(line)
                            numpy_line = np.genfromtxt(this_line)
                            thisProbe.totalAv_I = numpy_line[6]
                            in_av_I_block = False

                    # Start of section containing Summary Data from SCALA
                    if 'Summary data' in line:
                        in_sum_data_block = True
                    if in_sum_data_block:
                        if in_table_1:
                            if line.startswith('Outlier'):
                                in_table_1 = False
                            else:
                                values = scalaNumbers_regex.search(line)
                                if values:
                                    (thisProbe.overall_summary.
                                                append(values.group(2)))
                                    (thisProbe.inner_shell_summary.
                                                append(values.group(5)))
                                    (thisProbe.outer_shell_summary.
                                                append(values.group(8)))
                        else:
                            if re.search('\s*Overall', line):
                                in_table_1 = True
                        if line.startswith('$$'):
                            in_sum_data_block = False

                    # Find B factor from Truncate log file
                    if 'B factor' in line:
                        bFactor = re.search(r'\s{2}([0-9]+(\.[0-9]+)?)', line)
                        thisProbe.wilsonB = bFactor.group(1)

            # Add Dose data for the probe
            for line in dose_data:
                #print int(line[0])
                if (thisProbe.probe_number is not None) and (
                int(line[0]) == (thisProbe.probe_number * 2 - 1)):
                        thisProbe.dwd = line[1]
                        thisProbe.ad_wc = line[2]
                        thisProbe.tad95 = line[3]
                        thisProbe.maxDose = line[4]

            crystal[thisProbe.probe_number] = thisProbe
    return crystal
