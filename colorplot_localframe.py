###############################################################################
# Routine to create colorplots (and cuts) for dynamical quantities
# @author Filipe Guimaraes
# @date 14.01.2019
################################################################################
import numpy as np                            # Numerical library
import sys                                    # System library (to read arguments from command line)
import filesop                                # Operations with the files
import change_frame  as cf                    # Transform to local frame of axis (mxs, mx(mxs), m)
import interpolation                          # Interpolation subroutine
import plot_colormap as pc                    # Plotting the colormap subroutine
import matplotlib as mpl                      # Plotting library
from matplotlib import rc                     # Improve math fonts
import parameters as prm
import cuts

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
# rc('font',**{'family':'serif','serif':['Palatino']})
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}']
# matplotlib.rcParams['text.latex.preamble'] = [r'\renewcommand{\seriesdefault}{\bfdefault}',r'\boldmath']
#matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
# rc('mathtext', default='regular')
# Default fonts
mpl.rcParams['font.size']        = 11
mpl.rcParams['font.family']      = 'Arial'
mpl.rcParams['figure.titlesize'] = 'large'
mpl.rcParams['axes.titlepad'] = 10
mpl.rcParams['lines.linewidth']  = 2
#Legends:
mpl.rcParams['legend.fontsize']  = 'medium'
mpl.rcParams['legend.fancybox'] = False
# rcParams['legend.loc'] = 'upper left'`
mpl.rcParams['legend.framealpha'] = None
mpl.rcParams['legend.edgecolor'] = 'inherit'
mpl.rcParams['legend.handlelength'] = 2
mpl.rcParams["font.weight"] = "bold"
mpl.rcParams["axes.labelweight"] = "bold"


################################################################################
# How to use the script
################################################################################
def usage():
   """ Prints usage info and exists. """
   print("Files required. Use:")
   print("ipython colorplot_localframe.py 'filenames_x' 'filenames_y' 'filenames_z' (...)")
   print("where 'filenames_a' includes the a-component of the quantity to be plotted. E.g.:")
   print("ipython ~/programs/scripts/colorplot.py results/TSOC/5Npl/SOT/SOTx results/TSOC/5Npl/SOT/SOTy results/TSOC/5Npl/SOT/SOTz")
   print("The number of arguments will give the number of graphs plotted.")
   print("Wildcards can be used inside quotation marks.")
   print("Options can be chosen inside the script.")
   sys.exit()


################################################################################
# Main program
################################################################################
if __name__ == "__main__":
  # Check if files are given
  if(len(sys.argv) < 2):
    usage()

  # Check if multiple of 3 files are given (to make transformation to local frame)
  if len(sys.argv[1:])%3 != 0 and prm.local :
    print("Error: 3 components are needed to transform to the local frame of reference!")
    usage()

  # Number of plots
  num_plots = len(sys.argv[1:])
  # Number of rows and cols
  nrows = (num_plots-1)//prm.ncol+1
  ncols = min(num_plots,prm.ncol)

  # Building conversion matrix and reading information from files
  files = []
  values =[]
  x, y = ([ None for i in range( num_plots ) ] for _ in range(2))
  ij_to_arg = np.zeros((nrows,ncols), dtype=np.int)
  arg = 0
  for i in range(nrows):
    for j in range(ncols):
      ij_to_arg[i,j] = arg

      files.append( filesop.get_filenames(sys.argv[arg+1]) )
      # Field, Frequency, (columns to plot), mtheta, mphi
      values.append( filesop.get_values(prm.field_component[arg],files[arg],prm.double_angles) )

      # Next argument
      arg = arg + 1

  # Transforming from global to local frame of reference
  values_local = [ None for i in range( num_plots ) ]
  for i in range(nrows):
    i0 = i*ncols
    i1 = (i+1)*ncols
    values_local[i0:i1] = cf.global_to_local(values[i0:i1],prm.deltas,prm.local)
  
################################ CUTS ##########################################
  if prm.make_cuts:
    print("Creating cuts...")
    # Get all the points with values closest to the given ones
    cut_data = []
    for values in values_local:
      cut_data.append( cuts.get_cuts( values , prm.comp , prm.cuts ) )

    # Reorganizing data to be plotted
    plt_cut_x , plt_cut_y = ( [ [ [] for j in range(ncols) ] for i in range(len(values_local[0][0])-4) ] for _ in range(2) ) 
    for i in range(nrows):
      for j in range(ncols):
        for k in range(len(prm.cuts)): # Different cuts chosen in input
          for l in range(len(cut_data[ij_to_arg[i,j]][k][0])-4):
            # Transforming list to array to be able to transpose 
            ncuts = np.array(cut_data[ij_to_arg[i,j]][k]).T
            # Appending x and y of each line (angular rotation) and each cut defined in input
            # for each column (component of quantity) and each quantity (real, imaginary...)
            plt_cut_x[l][j].append( ncuts[-prm.comp+1].tolist() )
            plt_cut_y[l][j].append( ncuts[l+2].tolist() )
    # Create 'len(plt_cut_y)' figures with cuts plotted in 'ncols' columns
    cuts.plot_cuts( len(plt_cut_y) , ncols , plt_cut_x , plt_cut_y )

############################# COLORMAPS ########################################
  if prm.make_cm:
    print("Plotting colormaps...")
    # Interpolating and transposing i,j -> j,i
    z_old = [ [ None for j in range(len(values_local[0][0])-4) ] for i in range( num_plots ) ]
    for i in range(nrows):
      for j in range(ncols):
        # x[ij_to_arg[i,j]], y[ij_to_arg[i,j]], z_old[ij_to_arg[i,j]] = interpolation.interpolate(values_local[ij_to_arg[i,j]])
        x[ij_to_arg[j,i]], y[ij_to_arg[j,i]], z_old[ij_to_arg[j,i]] = interpolation.interpolate(values_local[ij_to_arg[i,j]])

    # Reshaping z[numplots][numfigs] -> z[numfigs][numplots]
    z = [ [ None for i in range( num_plots ) ] for j in range(0,len(values_local[0][0])-4) ]
    for i in range(nrows):
      for j in range(ncols):
        for fg in range(len(values_local[0][0])-4):
          z[fg][ij_to_arg[i,j]] = z_old[ij_to_arg[i,j]][fg]

    # Getting minimum and maximum for each row
    zmin, zmax = ([ None for i in range(len(values_local[0][0])-4) ] for _ in range(2))
    for k in range(len(values_local[0][0])-4):
      zmin[k] = [min([ j.min() for j in z[k][ncols*i:ncols*(i+1)] ]) for i in range(0,nrows)]
      zmax[k] = [max([ j.max() for j in z[k][ncols*i:ncols*(i+1)] ]) for i in range(0,nrows)]

    #Plotting colormap
    pc.plot_colormap(nrows,ncols,x,y,z,zmin,zmax)

    # Custom colorplot
    # Adding results to be plotted
    xs=[]
    ys=[]
    zs=[]
    zsmin=[]
    zsmax=[]
    xs.append( x[ij_to_arg[0,0]]    )
    ys.append( y[ij_to_arg[0,0]]    )
    zs.append( (z[1][ij_to_arg[1,0]]/ z[1][ij_to_arg[0,0]]) )
    zsmin.append( -1.e2 )
    zsmax.append( 1.e2 )

    xs.append( x[ij_to_arg[0,0]]    )
    ys.append( y[ij_to_arg[0,0]]    )
    zs.append( (z[0][ij_to_arg[1,0]]/ z[0][ij_to_arg[0,0]]) )
    zsmin.append( zs[1].min() )
    zsmax.append( zs[1].max() )

    xs.append( x[ij_to_arg[0,0]]    )
    ys.append( y[ij_to_arg[0,0]]    )
    zs.append( (z[2][ij_to_arg[1,0]]/ z[2][ij_to_arg[0,0]]) )
    zsmin.append( zs[2].min() )
    zsmax.append( zs[2].max() )

    xlabels=[r'$\theta$ (degrees)', r'$\theta$ (degrees)', r'$\theta$ (degrees)']
    ylabels=[r'Frequency (THz)', r'Frequency (THz)', r'Frequency (THz)']
    clabels=[r'$\hat{\tau}^\text{in-phase}_\text{DL}/\hat{\tau}^\text{in-phase}_\text{FL}$', r'$\hat{\tau}^\text{out-phase}_\text{DL}/\hat{\tau}^\text{out-phase}_\text{FL}$', r'$|\hat{\tau}_\text{DL}|/|\hat{\tau}_\text{FL}|$']
    titles=[r'$z\rightarrow y$',r'$z\rightarrow y$',r'$z\rightarrow y$']
    pc.plot_custom_colormap(1,len(zs),xs,ys,zs,zsmin,zsmax,xlabels,ylabels,clabels,titles,prm.output_prefix+'_ratio.pdf')

    # # Adding results to be plotted
    # xs=[]
    # ys=[]
    # zs=[]
    # zsmin=[]
    # zsmax=[]
    # xs.append( x[ij_to_arg[0,0]]    )
    # ys.append( y[ij_to_arg[0,0]]    )
    # zs.append( z[3][ij_to_arg[0,0]] )
    # zsmin.append( zs[0].min() )
    # zsmax.append( zs[0].max() )

    # xs.append( x[ij_to_arg[1,0]]    )
    # ys.append( y[ij_to_arg[1,0]]    )
    # zs.append( z[3][ij_to_arg[1,0]] )
    # zsmin.append( zs[1].min() )
    # zsmax.append( zs[1].max() )

    # xlabels=[r'$\theta$ (degrees)', r'$\theta$ (degrees)']
    # ylabels=[r'Frequency (THz)', r'Frequency (THz)']
    # clabels=[r'Phase $\varphi^\text{SOI}_\text{Fe,FL}$', r'Phase $\varphi^\text{SOI}_\text{Fe,DL}$']
    # titles=[r'$z\rightarrow y$',r'$z\rightarrow y$']
    # pc.plot_custom_colormap(1,len(zs),xs,ys,zs,zsmin,zsmax,xlabels,ylabels,clabels,titles,'SOT_phases.pdf')

    # Adding results to be plotted
    # xs=[]
    # ys=[]
    # zs=[]
    # zsmin=[]
    # zsmax=[]
    # xs.append( x[ij_to_arg[1,2]]    )
    # ys.append( y[ij_to_arg[1,2]]    )
    # zs.append( z[1][ij_to_arg[1,2]] )
    # zsmin.append( zs[0].min() )
    # zsmax.append( zs[0].max() )

    # # xs.append( x[ij_to_arg[1,0]]    )
    # # ys.append( y[ij_to_arg[1,0]]    )
    # # zs.append( z[3][ij_to_arg[1,0]] )
    # # zsmin.append( zs[1].min() )
    # # zsmax.append( zs[1].max() )

    # xlabels=[r'$\theta$ (degrees)', r'$\theta$ (degrees)']
    # ylabels=[r'Frequency (THz)', r'Frequency (THz)']
    # clabels=[r'Phase $\varphi^\text{SOI}_\text{Fe,FL}$', r'Phase $\varphi^\text{SOI}_\text{Fe,DL}$']
    # titles=[r'$z\rightarrow y$',r'$z\rightarrow y$']
    # pc.plot_custom_colormap(1,len(zs),xs,ys,zs,zsmin,zsmax,xlabels,ylabels,clabels,titles,'Beff_custom.pdf')
