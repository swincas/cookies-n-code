
import json
import math
import os
import random

import getdist
import getdist.plots

import matplotlib.pyplot as pyplot
import numpy
import pymultinest

#
# Model parameter information
#

params_min = [
    0, 
    0, 
    50,
    0
]

params_max = [
    1000,
    1000,
    1000,
    1000
]

params_count = len(params_min)

#
# Dataset information
#

data_length = 1000
xdata = numpy.empty(data_length)
ydata = numpy.empty(data_length)
ydata_err = numpy.empty(data_length)


#
# Evaluate gaussian function of 4 parameters (a, b, c, d)
# at point x
#

def evaluate_gaussian(x, a, b, c, d):
    return a * math.exp(-((x-b)*(x-b))/(2*c*c)) + d


#
# Calculate parameter values from the 'unit cube' by 
# taking into  account the paramete prior information.
#

def my_prior(cube, ndim, nparams):
    for i in range(ndim):
        cube[i] = params_min[i] + (params_max[i] - params_min[i]) * cube[i]


#
# Calculate the negative log likelihood given a set of 
# parameter values and the data.
#

def my_loglike(cube, ndim, nparams):
    
    # Extract the model parameter values
    a = cube[0]
    b = cube[1]
    c = cube[2]
    d = cube[3]
    
    # Allocate an array to store our model
    model_ydata = numpy.empty(data_length)
    
    # Evaluate our model
    for i in range(len(ydata)):
        model_ydata[i] = evaluate_gaussian(xdata[i], a, b, c, d)
    
    # Calculate weighted chi-squared
    chi2 = 0
    for i in range(len(ydata)):
        chi2 += ((model_ydata[i] - ydata[i]) / ydata_err[i])**2
    
    # Calculate negative log likelihood
    loglike = - 0.5 * chi2
    
    # At last, we are done!
    return loglike


def main():
    
    # Generate the x values of our data
    for i in range(len(xdata)):
        xdata[i] = float(i)
    
    # Set the noise stddev of the y values
    for i in range(len(ydata)):
        ydata_err[i] = 100.0
    
    params_value = [
        900,
        400,
        100,
        0
    ]
    # Generate the y values of our data
    for i in range(len(ydata)):
        # Evaluate gaussian
        ydata[i] = evaluate_gaussian(xdata[i], 
                                     params_value[0],
                                     params_value[1],
                                     params_value[2],
                                     params_value[3])
        # Add noise
        ydata[i] += random.gauss(0, ydata_err[i])
    
    filename = 'output/out'
    
    if not os.path.exists('./output'):
        os.makedirs('./output')
    
    # Run MultiNest!
    pymultinest.run(my_loglike, 
                    my_prior, 
                    params_count, 
                    outputfiles_basename=filename, 
                    resume=False, 
                    verbose=True,
                    importance_nested_sampling=True,
                    multimodal=False,
                    const_efficiency_mode=False,
                    n_live_points=100,
                    evidence_tolerance=0.3,
                    sampling_efficiency=0.8,
                    max_iter=0)
    
    # Perform result analysis
    analyzer = pymultinest.Analyzer(outputfiles_basename=filename, n_params=params_count)
    stats = analyzer.get_stats()
    
    # Pretty print results to a JSON file
    results_json = json.dumps(stats, sort_keys=True, indent=2)
    with open('pretty_results.json', 'w') as f:
        f.write(results_json)
      
    # Generate best-fit model
    ydata_best_fit = numpy.empty(data_length)
    for i in range(len(ydata_best_fit)):
        ydata_best_fit[i] = evaluate_gaussian(xdata[i],
                                              stats['modes'][0]['maximum'][0],
                                              stats['modes'][0]['maximum'][1],
                                              stats['modes'][0]['maximum'][2],
                                              stats['modes'][0]['maximum'][3])
    
    # Plot data vs best fit
    fig = pyplot.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(ydata, color='#5e3c99')
    ax.plot(ydata_best_fit, color='#e66101', linewidth=6)
    pyplot.savefig('data_vs_best_fit.png')
    
    # Corner plot
    samples = getdist.loadMCSamples(filename+'.txt')
    plotter = getdist.plots.getSubplotPlotter()
    plotter.triangle_plot([samples], filled=True)
    plotter.export('corner_plot.png')


if __name__ == '__main__':
    main()
