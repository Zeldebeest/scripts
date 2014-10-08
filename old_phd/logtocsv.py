'''
Simple script that parses log files and RADDOSE-3D output files to
a CSV summary in the form:
name, probe #, tad95, dwd, ad_wc, maxDose, I, I_resBin[nbins]
'''

import os
import numpy as np
from StringIO import StringIO
import re
import argparse
import csv


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
            with open(folder + '/' + current_log_file, 'r') as dose_array:
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

            with open(folder + '/' + current_log_file, 'r') as current_log:
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

parser = argparse.ArgumentParser(description='get the folder name')
parser.add_argument('foldername',help='gets the folder name')
parser.add_argument('-o', help='output file name')
parser.add_argument('-tag', default='crystalID')

args = parser.parse_args()

outputFile = args.o
this_crystal = processFolderWithACrystal(args.foldername, args.tag)

if not os.path.exists(outputFile):
    with open(outputFile, 'w') as outFile:
        csv_writer = csv.writer(outFile, delimiter=',')
        csv_writer.writerow(['crystal', 'probe', 'DWD', 'TAD', 'AD-WC', 'Max Dose',
                        'Total I/I_1', '5.7', '4', '3.3', '2.85', '2.55', '2.32',
                        '2.15', '2.01', '1.9', '1.8'])

with open(outputFile, 'a') as outFile: #append so that you can do multiple ones
    csv_writer = csv.writer(outFile, delimiter=',')
    
    go_on = False
    for key, probe in sorted(this_crystal.iteritems()):   
        resAv_I = []
        for resbin in probe.av_I_data[1:]:
            resAv_I.append(resbin[2])
        if probe.probe_number == 1:
            I_0 = probe.totalAv_I
            go_on = True
        if go_on is True:
            #print probe.probe_number
            list_to_print = [args.tag,
                   probe.probe_number,
                   probe.dwd,
                   probe.tad95,
                   probe.ad_wc,
                   probe.maxDose,
                   probe.totalAv_I/I_0]
            for item in resAv_I:
                list_to_print.append(item)
            csv_writer.writerow (list_to_print)
                    
print 'done'
