'''
Inspect calibrated dataset. Check for suspicious visibilities shown in weblog.

Last Modified: 16 Dec 2015

e.g.:
1. antenna 18: plotms() using column = 'DATA' (i.e. before calibration), amp v.s. time, iter baseline, average frequency.
   - if the amp. looks like noise --> flag it out

2. source: plotms() using column='corrrected', amp. v.s. uvdist, average time, check cross-scan time, average freq (avgchannel='64'), coloraxis='spw'. Check for high amp points, seems to be of the same spw, maybe just 1 baseline (as these high points appear sparse in uvdist)

3. calibrators: amp v.s. uvdist, check if the offset in amp. is due to different basebands with frequency offset --> steep spectral index causing an offset.


Note:
----
1. looks normal, points are not at noise level
2. don't see those high amp. points anymore, are they flagged by the pipeline?
3. amp. offset is due to band separation and steep source spectrum
'''


calfile = '../Imaging/3C220.3CAL.ms'
default(plotms)

# 1.
plotms(vis=calfile, xaxis='time', yaxis='amp', ydatacolumn='data', averagedata=True, avgchannel='64', iteraxis='baseline')

# 2.
plotms(vis=calfile,xaxis="uvwave",xdatacolumn="",yaxis="amp",ydatacolumn="corrected", selectdata=True,field="2", correlation="LL,RR", averagedata=True,avgchannel="64",avgtime="1e8s", avgscan=False,avgfield=False,avgbaseline=False,avgantenna=False,avgspw=False, scalar=False,transform=False,freqframe="",restfreq="",veldef="RADIO",coloraxis="spw",title="Field 2, 3C220.3")

# 3.
plotms(vis=calfile,xaxis="uvwave",xdatacolumn="",yaxis="amp",ydatacolumn="corrected", selectdata=True,field="0", correlation="LL,RR", averagedata=True,avgchannel="64",avgtime="1e8s", avgscan=False,avgfield=False,avgbaseline=False,avgantenna=False,avgspw=False, scalar=False,transform=False,freqframe="",restfreq="",veldef="RADIO",coloraxis="spw",title="Field 0, 3C147_flux")


plotms(vis=calfile,xaxis="uvwave",xdatacolumn="",yaxis="amp",ydatacolumn="corrected", selectdata=True,field="1", correlation="LL,RR", averagedata=True,avgchannel="64",avgtime="1e8s", avgscan=False,avgfield=False,avgbaseline=False,avgantenna=False,avgspw=False, scalar=False,transform=False,freqframe="",restfreq="",veldef="RADIO",coloraxis="spw",title="Field 1, J1153+8058_SNR")




