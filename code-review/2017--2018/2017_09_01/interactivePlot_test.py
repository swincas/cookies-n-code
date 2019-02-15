# import os, sys, random
import glob
import pyfits
import numpy as np
from interactivePlot_def import *

GalName = 'NGC5866'
data=pyfits.getdata(glob.glob('PXF_*'+GalName+'*.fits')[0], 0)

vel_sys = 755.

X, Y=data['xs'], data['ys']
Vel, VelErr=data['vpxf']-vel_sys, data['evpxf']
Sig, SigErr=data['spxf'], data['espxf']
SN = data['flux']

Sel = np.where(Sig > 0.)
SelectionWithoutDust = PlotPointSelector(X, Y, Sig, Sel)

X_Out, Y_Out, Vel_Out, VelErr_Out, Sig_Out, SigErr_Out, SN_Out = X[SelectionWithoutDust], Y[SelectionWithoutDust], Vel[SelectionWithoutDust], \
VelErr[SelectionWithoutDust], Sig[SelectionWithoutDust], SigErr[SelectionWithoutDust], SN[SelectionWithoutDust]

np.savetxt('OutputFile.txt', np.c_[X_Out, Y_Out, Vel_Out, VelErr_Out, Sig_Out, SigErr_Out, SN_Out])