###############################################################################
# Routine to create colorplots for dynamical quantities
# @author Filipe Guimaraes
# @date 14.01.2019
################################################################################
import numpy as np                            # Numerical library
import sys                                    # System library (to read arguments from command line)
import filesop                                # Operations with files
import interpolation                          # Interpolation subroutine
from matplotlib.pyplot import *               # Plotting library
import matplotlib.pyplot as plt               # Plotting library
import matplotlib.colors as colors            # Color selection and manipulation
from matplotlib import rc                     # Improve math fonts
from matplotlib.pyplot import cm              # Import colormap
from mpl_toolkits.axes_grid1 import AxesGrid  # Grid plotting
import scipy.interpolate                      # Interpolation library
from string import ascii_lowercase

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
# rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)
# matplotlib.rcParams['text.latex.preamble'] = [r'\renewcommand{\seriesdefault}{\bfdefault}',r'\boldmath']
#matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
# rc('mathtext', default='regular')
# Default fonts
rcParams['font.size']        = 12
rcParams['font.family']      = 'Arial'
rcParams['figure.titlesize'] = 'large'
rcParams['lines.linewidth']  = 2
#Legends:
rcParams['legend.fontsize']  = 'medium'
rcParams['legend.fancybox'] = False
# rcParams['legend.loc'] = 'upper left'`
rcParams['legend.framealpha'] = None
rcParams['legend.edgecolor'] = 'inherit'
rcParams['legend.handlelength'] = 2
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

################################################################################
# Setup and definitions
################################################################################
# Output filename
# output_file= 'Beff_2.pdf'
# DPI for the quality of the plotted figure
fig_dpi=200                

###### Setup what to plot:
field_component=[ 1, 1, 2, 1, 1, 2, 1, 1, 2 ]     
# 0-hwa, 1-hwt, 2-hwp
column_to_plot=2     
# 1-amplitude, 2-real part, 3-imaginary part, 4-phase, 5-cosine, 6-sine

###### Graph appearance and attributes:
# Double angles to 360 degrees or not:
double_angles=True
# Number of columns to be used in the figure
ncol=3
# y-label for each line
ylabel = [r'Frequency (THz)', r'Frequency (THz)', r'Frequency (THz)']
# Maximum y (frequency) value
ymax = 3.5
# x labels for each graph
xlabel = [r'$\theta$ (degrees)', r'$\theta$ (degrees)', r'$\phi$ (degrees)', 
          r'$\theta$ (degrees)', r'$\theta$ (degrees)', r'$\phi$ (degrees)', 
          r'$\theta$ (degrees)', r'$\theta$ (degrees)', r'$\phi$ (degrees)']
# colormap label for each line
clabel = [r'Effective Field (z$\rightarrow$ y)',
          r'Effective Field (z$\rightarrow$ x)',
          r'Effective Field (y$\rightarrow$ x)']
# Colormap 
colormap='RdBu'
# colormap='seismic_r'
linewidth=1.5

################################################################################
# How to use the script
################################################################################
def usage():
   """ Prints usage info and exists. """
   print("Files required. Use:")
   print("ipython colorplot.py 'filenames1' 'filenames2' (...)")
   print("where 'filenamesX' includes the quantity to be plotted. E.g.:")
   print("ipython ~/programs/scripts/colorplot.py results/TSOC/5Npl/SOT/SOTx results/TSOC/5Npl/SOT/SOTy results/TSOC/5Npl/SOT/SOTz")
   print("The number of arguments will give the number of graphs plotted.")
   print("Wildcards can be used inside quotation marks.")
   print("Options can be chosen inside the script.")
   sys.exit()


################################################################################
# Get the data from the file and save it into a matrix
################################################################################
def read_data_from_file(file):
  # Reading the data from the file
  data = pd.read_csv(file,
                     skiprows=1,
                     header=None,
                     delim_whitespace=True,
                     usecols=[0,column_to_plot]).values
  ndata = np.array(data)
  return ndata



################################################################################
# Get the desired values from the files
################################################################################
def get_values(arg,files):
  # Loop over the files in each argument
  values = []
  for filename in files:
    # Get the value of the field from the filename
    field = get_field_from_name(filename)
    # Get the required data from the file
    ndata = read_data_from_file(filename)
    # Building the two-dimension variable to be plotted
    for line in ndata:
      # print field_component, line
      values.append((field[field_component[arg]],line[0],line[1] ))
      if (double_angles==True) and (field[field_component[arg]] != 1.0):
        # print 360.0-field[field_component] , line[0] , line[1]
        values.append( ( 2.0-field[field_component[arg]] , line[0] , line[1] ) )
  return values

################################################################################
# Function to plot the colormap
################################################################################
def interpolate(values):
  # Sorting values
  values.sort()

  # Separating the values for the fit
  x = np.array([v[0] for v in values])*180                 # Transforming to degrees
  y = np.array([v[1] for v in values])*13.6*1000/4.135667  # Transforming to Frequency (THz)
  z = np.array([v[2] for v in values])

  # Getting number of points in x and y: nx repetitions of y[0]
  nx = sum(y == y[0])
  ny = len(x)/nx
  # Removing repetitions
  x = x[::ny]
  y = y[:ny]
  z.shape = (nx, ny)

  # Interpolation for data on rectangular grids using a bivariate cubic spline
  f = scipy.interpolate.RectBivariateSpline(x, y, z)

  # Getting new interpolated values (tenfold points on each axis, 
  # adjust this depending on the input file)
  x = np.linspace(x.min(), x.max(), 10*nx)
  y = np.linspace(y.min(), y.max(), 10*ny)
  z = f(x, y).transpose()
  return x, y, z

################################################################################
# set the colormap and centre the colorbar
# Obtained from:
# https://stackoverflow.com/a/50003503/3142385
################################################################################
class MidpointNormalize(colors.Normalize):
  def __init__(self, vmin, vmax, midpoint=0, clip=False):
    self.midpoint = midpoint
    colors.Normalize.__init__(self, vmin, vmax, clip)

  def __call__(self, value, clip=None):
    normalized_min = max(0.0, 1.0 / 2.0 * (1.0 - abs((float(self.midpoint) - float(self.vmin)) / (float(self.midpoint) - float(self.vmax)))))
    normalized_max = min(1.0, 1.0 / 2.0 * (1.0 + abs((float(self.vmax) - float(self.midpoint)) / (float(self.midpoint) - float(self.vmin)))))
    normalized_mid = 0.5
    x, y = [self.vmin, self.midpoint, self.vmax], [normalized_min, normalized_mid, normalized_max]
    return np.ma.masked_array(np.interp(value, x, y))

################################################################################
# Function to plot the colormap
################################################################################
def plot_colormap(x,y,z):
  # Loop over rows
  for i in range(0,nrows):
    # Create a grid with 'nrows' rows and 1 coluumn (using plot), each with size 1x'ncols' (using nrows_ncols)
    plot = nrows*100 + 10 + (i+1)
    grid[i] = AxesGrid(fig, plot, 
                       nrows_ncols=(1, ncols), 
                       axes_pad=0.3, 
                       share_all=True,
                       cbar_mode='single', 
                       cbar_location='right', 
                       cbar_pad=0.2 )
    # Loop over columns
    for j in range(0,ncols):
      im = grid[i][j].pcolormesh(x[ij_to_arg[i,j]], y[ij_to_arg[i,j]], z[ij_to_arg[i,j]],
                                 cmap=colormap, vmin=zmin[i], vmax=zmax[i], 
                                 norm=MidpointNormalize(vmin=zmin[i], vmax=zmax[i], midpoint=0), 
                                 rasterized=True)

      grid[i][j].set_xticks( np.arange(x[ij_to_arg[i,j]].min(), x[ij_to_arg[i,j]].max()+0.0001, 90) )
      # ax.xaxis.labelpad = -1
      grid[i][j].set_ylim( 0.0, ymax )
      grid[i][j].set_aspect(np.diff(grid[i][j].get_xlim())/np.diff(grid[i][j].get_ylim()))
      if j == 0:
        grid[i][j].set_ylabel(ylabel[i])
      grid[i][j].set_xlabel(xlabel[ij_to_arg[i,j]])
      for axis in ['top','bottom','left','right']:
        grid[i][j].spines[axis].set_linewidth(linewidth)
      grid[i][j].tick_params(axis='x', colors='black',width=linewidth)
      grid[i][j].tick_params(axis='y', colors='black',width=linewidth)
      # Add letters to each plot:
      grid[i][j].text(0.0, 1.03*ymax, letters[ij_to_arg[i,j]])

    grid[i].cbar_axes[0].colorbar(im)
    grid[i].cbar_axes[0].tick_params(width=2,colors='black')
    grid[i].cbar_axes[0].set_ylabel(clabel[i])
    grid[i].cbar_axes[0].ticklabel_format(style='sci', scilimits=(0,0))
    grid[i].cbar_axes[0].yaxis.set_offset_position('left')
    for axis in ['top','bottom','left','right']:
        grid[i].cbar_axes[0].spines[axis].set_linewidth(linewidth)
  return


if __name__ == "__main__":
  # Check if files are given
  if(len(sys.argv) < 2):
    usage()

  # Number of plots
  num_plots = len(sys.argv[1:])
  # Number of rows and cols
  nrows = (num_plots-1)//ncol+1
  ncols = min(num_plots,ncol)

  # Starting figure
  fig = plt.figure(figsize=(3*ncols+1, 3*nrows))
  grid = [ None for i in range( nrows ) ]
  letters = [(r'\textbf{'+ascii_lowercase[_]+')}') for _ in range(num_plots)]

  # Building conversion matrix and getting color range for each line
  files = []
  values =[]
  x, y, z = ([ None for i in range( num_plots ) ] for _ in range(3))
  ij_to_arg = np.zeros((nrows,ncols), dtype=np.int)
  arg = 0
  for i in range(0,nrows):
    for j in range(0,ncols):
      ij_to_arg[i,j] = arg

      files.append( filesop.get_filenames(sys.argv[arg+1]) )
      values.append( filesop.get_values(prm.field_component[arg],files[arg],prm.double_angles) )
      x[arg], y[arg], z[arg] = interpolate(values)

      # Next argument
      arg = arg + 1

  # Getting minimum and maximum for each row
  zmin = [min([j.min() for j in z[ncols*i:ncols*(i+1)]]) for i in range(0,nrows)]
  zmax = [max([j.max() for j in z[ncols*i:ncols*(i+1)]]) for i in range(0,nrows)]

  #Plotting colormap
  plot_colormap(x,y,z)

  plt.tight_layout()
  try: 
    output_file
  except NameError:
    plt.show()
  else:
    fig.savefig(output_file,transparent=True,dpi=fig_dpi, bbox_inches='tight')

  

