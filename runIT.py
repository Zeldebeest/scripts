'''
Created on 5 Dec 2012

@author: linc2027
'''

import extractingData as extD
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
# from numpy.dual import norm
import os
# from extractingData import Crystal
from itertools import cycle 


directory = os.path.dirname('runIT.py')
allXtalDir = os.path.join(directory, 'Individual-Crystals')
globalBeamDor = os.path.join(directory, 'Summed-Crystals')
#print directory

# import code
allKeys = {'P3S1':  [os.path.join(directory, "..\\BigBeam\\P3S1"),  'Large'],
           'P2S5':  [os.path.join(directory, "..\\BigBeam\\P2S5"),  'Large'],
           'P3S3':  [os.path.join(directory, "..\\BigBeam\\P3S3"),  'Large'],
           'P3S9':  [os.path.join(directory, "..\\BigBeam\\P3S9"),  'Large'],
           'P3S10': [os.path.join(directory, "..\\BigBeam\\P3S10"), 'Large'],
           '55':    [os.path.join(directory, "..\\MidBeam\\55"), 'Medium'],
           '197':   [os.path.join(directory, "..\\MidBeam\\197"),   'Medium'],
           '5185':  [os.path.join(directory, "..\\MidBeam\\5185"),  'Medium'],
          # 'P1S7':  ["H:\\MidBeam\\P1S7",  'Medium'],
           'P1S10': [os.path.join(directory, "..\\MidBeam\\P1S10"), 'Medium'],
           'P3S2':  [os.path.join(directory, "..\\MidBeam\\P3S2"),  'Medium']
           }




# Dict with the key as [beamsize, xtal-name]: list-of-wedges
allCrystals = {}

for this_Key, this_Crystal in allKeys.iteritems():
    print 'Crystal object ' + this_Key + ' created'
    allCrystals[this_Crystal[1], this_Key] = \
    extD.processFolderWithACrystal(this_Crystal[0], this_Key)

#-----------------------------------------------------------------------------
# Aggregate plots:
#-----------------------------------------------------------------------------

plot_info = []
plot_info.append({'dose-type': 'ad_wc',
                  'x-axis': 'Average Dose, Whole Crystal'
                  })
plot_info.append({'dose-type': 'tad95',
                  'x-axis': 'Threshold Average Dose'
                  })
plot_info.append({'dose-type': 'maxDose',
                  'x-axis': 'Maximum Dose'
                  })
plot_info.append({'dose-type': 'dwd',
                  'x-axis': 'Diffraction Weighted Dose'
                  })

beam_sizes = [['large', 'Large Beam, all crystals'],
               ['Med', 'Medium Beam, all crystals']]

styles = cycle(['b1', 'g2', 'r3', 'c4', 'mo',
                'bv', 'g<', 'r>', 'c^', 'mx'])


figures = []

for this_beam_size in beam_sizes:
    for this_figure in plot_info:
        # Large beams:
        handle = this_figure['dose-type'] + '-' + this_beam_size[0]
        tempFig = plt.figure(handle)
        plt.xlabel('x-axis')
        plt.ylabel('$I/I_0$')
        plt.title(this_beam_size[1])
        figures.append({'beam': this_beam_size,
                        'dose_type': this_figure['dose-type'],
                        'figure': handle})

for  this_Key, this_Crystal in sorted(allCrystals.iteritems()):
#    print ('Crystal {} ({} beam)'.format(this_Key[1], this_Key[0]) +
#           'loaded for individual processing')
    # Change the plot tyoe here.
        for key, probe in sorted(this_Crystal.iteritems()):
            if key and probe.totalAv_I:
                if key == 1:
                    I_0 = probe.totalAv_I
#               print str(key) + ' and ' + str(probe)
                metrics = [probe.totalAv_I / I_0]
                for metric in metrics:
                    for fig in figures:
                        if this_Key[0] == 'Large' and fig['beam'][0] == 'large':

                         #   print getattr(probe, fig['dose_type'])
                         #   print '-------------'
                         #   print metric
                            plt.figure(fig['figure'])
                            fig['dose_type']
                            plt.plot(getattr(probe, fig['dose_type']),
                                        metric)
                            plt.show()
                                        #styles.next())
                        if this_Key[0] == 'Medium' and fig['beam'] == 'Medium':
                            plt.figure(fig['handle'])
                            plt.plot(probe.fig['dose-type'],
                                     metric,
                                     styles.next())

print figures
for fig in figures:
    print fig
    fig = plt.figure(fig['figure'])
    plt.savefig('Overall-Decay-' +
                        '{}-{}.png'.format(this_Key[0],
                                           this_Key[1]),
                                           bbox_inches=0)
print 'Done'
