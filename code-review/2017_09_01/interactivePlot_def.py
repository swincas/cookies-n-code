import os, sys, random
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


def onclick(event):
  global coords
  try: length = len(coords)
  except: coords = []
  if event.button==1:
    print 'Point selected to remove: xdata=%f, ydata=%f'%(event.xdata, event.ydata)
    plt.scatter(event.xdata, event.ydata, s=50, marker = 'o', c='r')
    plt.draw()
    coords.append((event.xdata, event.ydata))


def PlotPointSelector(x, y, z, Sel):
  # making an interactive plot that enables points to be selected and then removed. 
  print 'Select points to be removed by clicking on them. '
  print 'Close the plot when selection is complete. '


  fig=plt.figure()
  ax=fig.add_subplot(111)
  cax=ax.scatter(np.array(x)[Sel], np.array(y)[Sel], c=np.array(z)[Sel], s=50, marker='o', \
    norm=mpl.colors.Normalize(vmin=np.min(np.array(z)[Sel]), vmax=np.max(np.array(z)[Sel])))
  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_xlim(max(np.array(x)[Sel])+5, min(np.array(x)[Sel])-5)
  cb1=fig.colorbar(cax)
  cb1.set_label('z')
  plt.title('Input data to be refined')

  # here recording the user interaction with the plot. 
  # 'onclick' defines a set of coordinates that the user has selected
  cid = fig.canvas.mpl_connect('button_press_event', onclick)
  plt.show()
  plt.close()

  # now I need to identify which array indices these selected coordinates relate to, 
  # by identifying the closest in x/y space
  Rejection = []
  for kk in range(len(coords)):
    DIFF = 100
    for jj in range(len(x)):
      if (np.sqrt((x[jj]-coords[kk][0])**2 + (y[jj]-coords[kk][1])**2) < DIFF):
        Rejection_element = jj
        DIFF = np.sqrt((x[jj]-coords[kk][0])**2 + (y[jj]-coords[kk][1])**2)
    Rejection.append(Rejection_element)
  Rejection = np.array(Rejection)

  Sel = np.array(Sel[0])

  # redefining the new Selection array such that the rejected points have been removed
  Sel = Sel[np.where(-(np.in1d(Sel, Rejection)))]

  if len(coords) > 0:
    fig=plt.figure()
    ax=fig.add_subplot(111)
    cax=ax.scatter(np.array(x)[Sel], np.array(y)[Sel], c=np.array(z)[Sel], s=50, marker='o', \
      norm=mpl.colors.Normalize(vmin=np.min(np.array(z)[Sel]), vmax=np.max(np.array(z)[Sel])))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(max(np.array(x)[Sel])+5, min(np.array(x)[Sel])-5)
    cb1=fig.colorbar(cax)
    cb1.set_label('z')
    
    plt.title('Refined output')
    plt.show()
    plt.close()
  return Sel # return the array of final 'acceped' indices


