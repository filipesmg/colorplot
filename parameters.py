################################################################################
# Setup and definitions
################################################################################
# Output filename
output_prefix= 'Beff_global'
# DPI for the quality of the plotted figure
fig_dpi=200         
stype = ['real','imag','ampl','phase']

###### Setup what to plot:
field_component=[ 1, 1, 1, 1, 1, 1, 2, 2, 2 ]     
# 0-hwa, 1-hwt, 2-hwp

# Transform to local frame of reference (mxs, mx(mxs), m):
local = False
# Spin accumulation direction:
deltas = [1.0,0.0,0.0]

# Number of columns to be used in the figure (multiple of 3)
ncol=3

# Double angles to 360 degrees or not:
double_angles=False

# Add prefactor 1/w
prefactor_frequency=True

#-------------------------- Graph appearance and attributes:--------------------
# Make colormaps or not
make_cm = True
# y-label for each line
ylabel = [r'Frequency (THz)', r'Frequency (THz)', r'Frequency (THz)']
# Maximum y (frequency) value
ymax = 2.1
# x labels for each graph
xlabel = [r'$\theta$ (degrees)', r'$\theta$ (degrees)', r'$\phi$ (degrees)', r'$\theta$ (degrees)', r'$\theta$ (degrees)', r'$\phi$ (degrees)', r'$\theta$ (degrees)', r'$\theta$ (degrees)', r'$\phi$ (degrees)']
# Title for each column
title = [r'$z\rightarrow y$',r'$z\rightarrow x$',r'$x\rightarrow y$']
# title = [r'Torque $\tau_x$ ',r'Torque $\tau_y$ ',r'Torque $\tau_z$ '])
# colormap label for each line
clabel_local = [r'Field-like Torque',r'Damping-like Torque',r'Longitudinal']
clabel_global = [r'$x$-component',r'$y$-component',r'$z$-component']
# Colormap 
colormap='RdBu_r'
# colormap='seismic'
# Linewidth of frame and ticks
linewidth=1.5
# Title size
titlesize=14

#-------------------------- Cuts:--------------------
# Make cuts or not
make_cuts = True
# Component to make the cut: 0 - field ; 1 - frequency
comp = 1
# Values to make the cuts
cuts = [0.0]
# Colors of cuts in each (must have the same amount of rotation directions: z->y, z->x, x->y):
colors=['g','r','b']
# Line styles for different values of cuts (must have the same amount of values as number of cuts):
linestyles=['solid'] # , 'dotted', 'dashdot' ]
