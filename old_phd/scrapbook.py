'''
Created on 19 Dec 2012

@author: Oliver
'''


    if this_Key[0] == 'Large':
                if dose_dict['shortTitle'] == 'AD-WC':
                    plt.figure('ADWC-Large')
                    plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
                    all_large_ADWC += norm_total_av_I
                    all_large_ADWC_doses += dose_dict['metric']
                if dose_dict['shortTitle'] == 'TAD-95':
                    plt.figure('TAD-Large')
                    plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
                    all_large_TAD += norm_total_av_I
                    all_large_TAD_doses += dose_dict['metric']
                if dose_dict['shortTitle'] == 'Max Dose':
                    plt.figure('MAX-Large')
                    plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
                    all_large_MAX += norm_total_av_I
                    all_large_MAX_doses += dose_dict['metric']
                if dose_dict['shortTitle'] == 'DWD':
                    plt.figure('DWD-Large')
                    plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
                    all_large_DWD += norm_total_av_I
                    all_large_DWD_doses += dose_dict['metric']

    if this_Key[0] == 'Medium':
                if dose_dict['shortTitle'] == 'AD-WC':
                    plt.figure('ADWC-Med')
                    plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
                    all_med_ADWC += norm_total_av_I
                    all_med_ADWC_doses += dose_dict['metric']
                if dose_dict['shortTitle'] == 'TAD-95':
                    plt.figure('TAD-Med')
                    plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
                    all_med_TAD += norm_total_av_I
                    all_med_TAD_doses += dose_dict['metric']
                if dose_dict['shortTitle'] == 'Max Dose':
                    plt.figure('MAX-Med')
                    plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
                    all_med_MAX += norm_total_av_I
                    all_med_MAX_doses += dose_dict['metric']
                if dose_dict['shortTitle'] == 'DWD':
                    plt.figure('DWD-Med')
                    plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
                    all_med_DWD += norm_total_av_I
                    all_med_DWD_doses += dose_dict['metric']
    
    # Set up as a list of dictionairies
    plotting_sets = [{'label': 'ADWC-Large',
                      'intensities': all_large_ADWC,
                      'doses': all_large_ADWC_doses},
                     {'label': 'TAD-Large',
                      'intensities': all_large_TAD,
                      'doses': all_large_TAD_doses},
                     {'label': 'MAX-Large',
                      'intensities': all_large_MAX,
                      'doses': all_large_MAX_doses},
                     {'label': 'DWD-Large',
                      'intensities': all_large_DWD,
                      'doses': all_large_DWD_doses},
                     {'label': 'ADWC-Med',
                      'intensities': all_med_ADWC,
                      'doses': all_med_ADWC_doses},
                     {'label': 'TAD-Med',
                      'intensities': all_med_TAD,
                      'doses': all_med_TAD_doses},
                     {'label': 'MAX-Med',
                      'intensities': all_med_MAX,
                      'doses': all_med_MAX_doses},
                     {'label': 'DWD-Med',
                      'intensities': all_med_DWD,
                      'doses': all_med_DWD_doses}
                      ]
    
    # Plot all crystals on one graph
    for av_plot in plotting_sets:
        plt.figure(av_plot['label'])
        m, b = np.polyfit(av_plot['doses'], av_plot['intensities'], 1)
        plt.plot(av_plot['doses'],
                 (m * np.array(av_plot['doses']) + b), '-r')
        I_corr_coeff = np.corrcoef(av_plot['doses'], av_plot['intensities'])
        plt.ylim(0, 1)
        plt.figtext(0.5, 0.75,
                            ('Correlation Coefficient: ' +
                             '{:.4}'.format(I_corr_coeff[0][1]) +
                             '\nIntercept: {:.2}\nGradient: {:.2}'.format(b, m) +
                             '\n$D_{1/2}$: ' + '{0:.2g} MGy'.format(((0.5 - b) / m)
                                                                    )
                             )
                            )
    
        title = av_plot['label']
        plt.savefig(title + '.png', bbox_inches=0)
      #  plt.savefig(title + '.pdf', bbox_inches=0)
      #  plt.savefig(title + '.svg', bbox_inches=0)
    



#-----------------------------------------------------------------------------
# Plot all the individual crystal data
#-----------------------------------------------------------------------------
if plot_individual:
    for  this_Key, this_Crystal in allCrystals.iteritems():
        print 'Crystal {} loaded for individual processing'.format(this_Key[1])
        #create, label etc.
        list_of_TotalAvI = []
        list_of_probe_number = []
        list_of_AvI = []
        list_of_B = []
        list_of_tad95 = []
        list_of_ad_wc = []
        list_of_maxDose = []
        list_of_dwd = []
        doOnce = True  # For grabbing bits needed for the surface plot

        for number, probe in this_Crystal.iteritems():
            if probe.totalAv_I:
                avIdata = np.array(probe.av_I_data[1:], dtype=float)
                if doOnce:
                    resBinLimits = avIdata[0:, 1]
                    doOnce = False
                list_of_AvI.append(avIdata[0:, 2])
                list_of_TotalAvI.append(float(probe.totalAv_I))
                list_of_B.append(float(probe.wilsonB))
                list_of_probe_number.append(float(probe.probe_number))
                list_of_tad95.append(probe.tad95)
                list_of_dwd.append(probe.dwd)
                list_of_ad_wc.append(probe.ad_wc)
                list_of_maxDose.append(probe.maxDose)
    
        #-----------------------------------------------------------
        # Stupid thing needs to be sorted.. (it defaults to
        #-----------------------------------------------------------
    
        xyzB = zip(list_of_probe_number,
                   np.array(list_of_AvI, dtype=float),
                   list_of_TotalAvI,
                   list_of_B,
                   list_of_tad95,
                   list_of_ad_wc,
                   list_of_maxDose,
                   list_of_dwd
                   )
        (sorted_list_probeNum,
         sorted_AvI,
         sorted_TotalAv,
         sorted_WB,
         sorted_tad95,
         sorted_ad_wc,
         sorted_maxDose,
         sorted_dwd) = \
        zip(*sorted(xyzB, key=lambda el: el[0]))

        adwc_params = {'metric': sorted_ad_wc,
                       'title': 'Average Dose, Whole Crystal',
                       'shortTitle': 'AD-WC'}
        maxDose_params = {'metric': sorted_maxDose,
                          'title': 'Maximum Dose',
                          'shortTitle': 'Max Dose'}
        tad95_params = {'metric': sorted_tad95,
                        'title': '95 % Threshold Average Dose',
                        'shortTitle': 'TAD-95'}
        dwd_params = {'metric': sorted_dwd,
                      'title': 'Diffraction Weighted Dose',
                      'shortTitle': 'DWD'}
        doses = [adwc_params, maxDose_params, tad95_params, dwd_params]
        # Normalise the total Av_I's
        norm_total_av_I = []
        for thisAvI in sorted_TotalAv:
            norm_total_av_I.append(thisAvI / sorted_TotalAv[0])

        # Normalise the res-wise Av I's
        norm_av_I = []
        for thisAvI in sorted_AvI:
            normThis = []
            i = 0
            for entry in thisAvI:
                if entry < 0:
                    normThis.append(0)
                else:
                    normThis.append(entry / sorted_AvI[0][i])
                i += 1
            norm_av_I.append(normThis)
    
        for dose_dict in doses:
            
            #-----------------------------------------------------------
            # Plotting Bin-wise decay,
            #-----------------------------------------------------------
    
            fig = plt.figure()
            ax = fig.gca(projection='3d')
    
            #X, Y = np.meshgrid(np.array(list_of_probe_number, dtype=float),
            #                   np.array(resBinLimits, dtype=float))
            #Z = np.array(list_of_AvI, dtype=float).reshape(X.shape)
    
            X, Y = np.meshgrid(np.array(resBinLimits, dtype=float),
                               sorted_list_probeNum)
    
            Z = norm_av_I
    
            surf = ax.plot_surface(X, Y, Z, rstride=1, shade=1, linewidth=1,
                                   cstride=1, cmap=cm.coolwarm)
    
            plt.title('Resolusion-wise intensity for crystal ' +
                      '{} with the {} beam'.format(this_Key[1], this_Key[0]))
            ax.set_xlabel('Edge of resolution Bin')
            ax.set_ylabel(dose_dict['title'])
            ax.set_zlabel('$I/I_0$')
            ax.set_zlim(0, 1)
    
            ax.view_init(elev=25, azim=160)
    
            plt.savefig('Bin-Wise-Decay-{}-{}.pdf'.format(this_Key[0], 
                                                          this_Key[1]),
                                                          bbox_inches=0)
            plt.savefig('Bin-Wise-Decay-{}-{}.png'.format(this_Key[0], 
                                                          this_Key[1]),
                                                          bbox_inches=0)
            plt.savefig('Bin-Wise-Decay-{}-{}.svg'.format(this_Key[0], 
                                                          this_Key[1]),
                                                          bbox_inches=0)
    
            #######################################################################
            # Plotting one linear fit for each crystal
            #######################################################################
    
            fig = plt.figure()
    
            plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
    
            plt.xlabel(dose_dict['title'])
            plt.ylabel('$I/I_0$')
    
            m, b = np.polyfit(dose_dict['metric'], norm_total_av_I, 1)
            plt.plot(dose_dict['metric'],
                     (m * np.array(dose_dict['metric']) + b), '--k')
            I_corr_coeff = np.corrcoef(dose_dict['metric'], norm_total_av_I)
            plt.ylim(0, 1)
            plt.figtext(0.5, 0.75,
                        ('Correlation Coefficient: ' +
                         '{:.4}'.format(I_corr_coeff[0][1]) +
                         '\nIntercept: {:.2}\nGradient: {:.2}'.format(b, m) +
                         '\n$D_{1/2}$: ' + '{0:.2g} MGy'.format(((0.5 - b) / m))
                         )
                        )
    
            plt.title('Overall intensity for crystal ' +
                      '{} with the {} beam'.format(this_Key[1], this_Key[0]))
    
            plt.savefig('Overall-Decay-' +
                        '{}-{}-{}.pdf'.format(dose_dict['shortTitle'],
                                              this_Key[0],
                                              this_Key[1]),
                                              bbox_inches=0)
            plt.savefig('Overall-Decay-' +
                        '{}-{}-{}.png'.format(dose_dict['shortTitle'],
                                              this_Key[0],
                                              this_Key[1]),
                                              bbox_inches=0)
            plt.savefig('Overall-Decay-' +
                        '{}-{}-{}.svg'.format(dose_dict['shortTitle'],
                                              this_Key[0],
                                              this_Key[1]),
                                              bbox_inches=0)
    
            #-----------------------------------------------------------
            # Plotting Total Average Decay - Two linear fits
            #-----------------------------------------------------------
            if len(dose_dict['metric']) > 6:
                fig = plt.figure()
    
                plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
                plt.xlabel(dose_dict['title'])
                plt.ylabel('$I/I_0$')
                plt.title('Overall intensity for crystal ' +
                          '{} with the {} beam'.format(this_Key[1], this_Key[0]))
    
                # for first Regime
                m, b = np.polyfit(dose_dict['metric'][:4], norm_total_av_I[:4], 1)
                plt.plot(dose_dict['metric'],
                         (m * np.array(dose_dict['metric']) + b), '--g')
                I_corr_coeff = np.corrcoef(dose_dict['metric'][:4],
                                           norm_total_av_I[:4])
                plt.ylim(0, 1)
                plt.figtext(0.5, 0.75,
                         ('Correlation Coefficient: ' +
                          '{:.4}'.format(I_corr_coeff[0][1]) +
                         '\nIntercept: {:.2}\nGradient: {:.2}'.format(b, m) +
                         '\n$D_{1/2}$: ' + '{0:.2g} MGy'.format((0.5 - b) / m)
                         ), color='green')
    
                # for second regime
                m, b = np.polyfit(dose_dict['metric'][5:], norm_total_av_I[5:], 1)
                plt.plot(dose_dict['metric'],
                         (m * np.array(dose_dict['metric']) + b), '--r')
                I_corr_coeff = np.corrcoef(dose_dict['metric'][5:],
                                           norm_total_av_I[5:])
                plt.figtext(0.5, 0.6,
                         ('Correlation Coefficient: ' +
                          '{:.4}'.format(I_corr_coeff[0][1]) +
                         '\nIntercept: {:.2}\nGradient: {:.2}'.format(b, m) +
                         '\n$D_{1/2}$: ' + '{0:.2g} MGy'.format((0.5 - b) / m)),
                            color='red')
    
                plt.savefig('Overall-Decay-two-fits-' +
                            '{}-{}-{}.pdf'.format(dose_dict['shortTitle'],
                                                  this_Key[0],
                                                  this_Key[1]),
                                                  bbox_inches=0)
                plt.savefig('Overall-Decay-two-fits-' +
                            '{}-{}-{}.png'.format(dose_dict['shortTitle'],
                                                  this_Key[0],
                                                  this_Key[1]),
                                                  bbox_inches=0)
                plt.savefig('Overall-Decay-two-fits-' +
                            '{}-{}-{}.svg'.format(dose_dict['shortTitle'],
                                                  this_Key[0], this_Key[1]),
                                                  bbox_inches=0)
    
            #-----------------------------------------------------------
            # Plotting Total Average Decay - Exponential fit
            #-----------------------------------------------------------
        
            fig = plt.figure()
        
            plt.plot(dose_dict['metric'], norm_total_av_I,  'rx')
            plt.xlabel(dose_dict['title'])
            plt.ylabel('$I/I_0$')
            plt.title('Overall intensity for crystal ' +
                      '{} with the {} beam'.format(this_Key[1], this_Key[0]))
        
            # take logs
            logI = np.log(norm_total_av_I)
            # for first Regime
            m, b = np.polyfit(dose_dict['metric'], logI, 1)
            plt.plot(dose_dict['metric'],
                     (b * np.exp(m * np.array(dose_dict['metric']))), '--k')
            plt.ylim(0, 1)
            I_corr_coeff = np.corrcoef(dose_dict['metric'], logI)
            plt.figtext(0.5, 0.8,
                     ('Correlation Coefficient: {:.4}'.format(I_corr_coeff[0][1])
                     + '\nIntercept: {:.2}\nDecay Constant: {:.2}'.format(b, m)))
        
            plt.savefig('Overall-Decay-exp-fits-{}-{}.pdf'.format(this_Key[0],
                        this_Key[1]),
                        bbox_inches=0)
            plt.savefig('Overall-Decay-exp-fits-{}-{}.png'.format(this_Key[0],
                        this_Key[1]),
                        bbox_inches=0)
            plt.savefig('Overall-Decay-exp-fits-{}-{}.svg'.format(this_Key[0],
                        this_Key[1]),
                        bbox_inches=0)
    
            #-----------------------------------------------------------
            # Plotting Wilson B
            #-----------------------------------------------------------
    
            fig = plt.figure()
            m, b = np.polyfit(dose_dict['metric'], sorted_WB, 1)
    
            plt.plot(dose_dict['metric'], sorted_WB,  'x')
            plt.plot(dose_dict['metric'],
                     (m * np.array(dose_dict['metric']) + b), '--k')
    
            plt.title('Wilson B-factor for crystal ' +
                      '{} with the {} beam'.format(this_Key[1], this_Key[0]))
            plt.xlabel(dose_dict['title'])
            plt.ylabel('Wilson B')
            WB_corr_coeff = np.corrcoef(dose_dict['metric'], sorted_WB)
            plt.figtext(0.5, 0.75,
                     ('Correlation Coefficient: {:.3}'.format(WB_corr_coeff[0][1])
                       + '\nIntercept: {:.2}\nGradient: {:.2}'.format(b, m)))
    
            plt.savefig('Wilson-B-{}-{}-{}.png'.format(dose_dict['shortTitle'],
                                                       this_Key[0], this_Key[1]),
                                                       bbox_inches=0)
            plt.savefig('Wilson-B-{}-{}-{}.pdf'.format(dose_dict['shortTitle'],
                                                       this_Key[0], this_Key[1]),
                                                       bbox_inches=0)
            plt.savefig('Wilson-B-{}-{}-{}.svg'.format(dose_dict['shortTitle'],
                                                       this_Key[0], this_Key[1]),
                                                       bbox_inches=0)
    

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------