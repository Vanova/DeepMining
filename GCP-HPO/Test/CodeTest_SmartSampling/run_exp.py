# Author: Sebastien Dubois 
#		  for ALFA Group, CSAIL, MIT

# The MIT License (MIT)
# Copyright (c) 2015 Sebastien Dubois

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append("../../")
from smart_sampling import smartSampling

### Set parameters ###
parameter_bounds = np.asarray( [[0,400]] )
nugget = 1.e-10
n_clusters = 1
cluster_evol ='constant'
corr_kernel = 'squared_exponential'
mapWithNoise= False
model_noise = None
sampling_model = 'GCP'
n_candidates= 300
n_random_init= 10
nb_GCP_steps = 6
nb_iter_final = 0
acquisition_function = 'MaxUpperBound'

def scoring_function(x):
    res = (70-7*np.exp(x/50. - ((x-55.)**2)/500.) + 6*np.sin(x/40.) +3./(1.1+np.cos(x/50.)) - 15./(3.3-3*np.sin((x-70)/25.)))/100.
    return [res]


X,Y = smartSampling(nb_GCP_steps,parameter_bounds,scoring_function,
											  isInt=True,
							                  corr_kernel = corr_kernel,
							                  acquisition_function = acquisition_function,
							                  GCP_mapWithNoise=mapWithNoise,
							          		  model_noise = model_noise,
							                  model = sampling_model, 
							                  n_candidates=n_candidates,
							                  n_random_init=n_random_init,
							                  n_final_iter=nb_iter_final,
							                  n_clusters=1, 
							                  cluster_evol = cluster_evol,
							                  verbose=True,
							                  detailed_res = False)

X = np.asarray(X[0])
Y = np.asarray(Y[0])

X_init = X[:n_random_init]
Y_init = Y[:n_random_init]

n_smart_steps = X.shape[0] - n_random_init
print n_smart_steps,'new tested points'

n_rows = n_smart_steps/3
if not(n_smart_steps% 3 == 0):
	n_rows += 1

# plot results
abs = range(0,400)
f_plot = [scoring_function(i) for i in abs]
fig = plt.figure()
plt.title('Smart sampling process')

for i in range(1,n_smart_steps+1):
	ax = fig.add_subplot(n_rows,3,i)
	ax.plot(abs,f_plot)
	ax.plot(X[:(n_random_init+i)],Y[:(n_random_init+i)],'ro',label='GCP query points')
	ax.plot(X_init,Y_init,'bo',label='Random initialization')

plt.legend()
plt.show()