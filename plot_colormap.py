import numpy as np                            # Numerical library
from mpl_toolkits.axes_grid1 import AxesGrid  # Grid plotting
import matplotlib.pyplot as plt               # Plotting library
import matplotlib.colors as colors            # Color selection and manipulation
from string import ascii_lowercase
import parameters as prm

################################################################################
# Function to plot the colormap
################################################################################
def plot_colormap(nrows,ncols,x,y,zs,zmin,zmax):
  # Starting figure
  fig = plt.figure(figsize=(3*ncols+1, 3*nrows))
  plt.subplots_adjust(hspace=0.3)
  grid = [ None for i in range( nrows ) ]
  letters = [(r'\textbf{'+ascii_lowercase[_]+')}') for _ in range(nrows*ncols)]
  for fg in range(len(zs)):
    # Loop over rows
    arg = 0
    for i in range(0,nrows):
      # Create a grid with 'nrows' rows and 1 coluumn (using plot), each with size 1x'ncols' (using nrows_ncols)
      plot = nrows*100 + 10 + (i+1)
      grid[i] = AxesGrid(fig, plot, 
                         nrows_ncols=(1, ncols), 
                         axes_pad=0.2,
                         share_all=True,
                         cbar_mode='single', 
                         cbar_location='right', 
                         cbar_pad=0.2 )
      # Loop over columns
      for j in range(0,ncols):
        im = grid[i][j].pcolormesh(x[arg], y[arg], zs[fg][arg], cmap=prm.colormap, vmin=zmin[fg][i], vmax=zmax[fg][i], norm=MidpointNormalize(vmin=zmin[fg][i], vmax=zmax[fg][i], midpoint=0), rasterized=True)

        grid[i][j].set_xticks( np.arange(x[arg].min(), x[arg].max()+0.0001, 90) )
        # ax.xaxis.labelpad = -1
        grid[i][j].set_ylim( 0.0, prm.ymax )
        grid[i][j].set_aspect(np.diff(grid[i][j].get_xlim())/np.diff(grid[i][j].get_ylim()))
        if j == 0:
          grid[i][j].set_ylabel(prm.ylabel[i])
        if i == 0:
          grid[i][j].set_title(prm.title[j], size=prm.titlesize)
        grid[i][j].set_xlabel(prm.xlabel[arg], labelpad=-0.05)
        for axis in ['top','bottom','left','right']:
          grid[i][j].spines[axis].set_linewidth(prm.linewidth)
        grid[i][j].tick_params(axis='x', colors='black',width=prm.linewidth)
        grid[i][j].tick_params(axis='y', colors='black',width=prm.linewidth)
        # Add letters to each plot:
        grid[i][j].text(0.0, 1.03*prm.ymax, letters[arg])
  	    # Next argument
        arg = arg + 1


      cb = grid[i].cbar_axes[0].colorbar(im)
      grid[i].cbar_axes[0].tick_params(width=2,colors='black')
      grid[i].cbar_axes[0].set_ylabel(prm.clabel_local[i] if prm.frame == "local" else prm.clabel_cartesian[i] if prm.frame == "cartesian" else prm.clabel_spherical[i], size=prm.titlesize)
      grid[i].cbar_axes[0].ticklabel_format(style='sci', scilimits=(0,0))
      grid[i].cbar_axes[0].yaxis.set_offset_position('left')
      cb.solids.set_rasterized(True) 
      for axis in ['top','bottom','left','right']:
          grid[i].cbar_axes[0].spines[axis].set_linewidth(prm.linewidth)

    # plt.tight_layout()
    fig.savefig(prm.output_prefix+'_'+prm.stype[fg]+'.pdf',transparent=True,dpi=prm.fig_dpi, bbox_inches='tight')
    plt.clf()
  return


################################################################################
# Function to plot a custom colormap
################################################################################
def plot_custom_colormap(nrows,ncols,x,y,zs,zsmin,zsmax,xlabels,ylabels,clabels,titles,filename):
  # Starting figure
  fig = plt.figure(figsize=(3*ncols+3, 3*nrows))
  plt.subplots_adjust(hspace=0.3)
  letters = [(r'\textbf{'+ascii_lowercase[_]+')}') for _ in range(nrows*ncols)]
  # Loop over rows
  arg = 0
  # Create a grid with 'nrows' rows and 1 coluumn (using plot), each with size 1x'ncols' (using nrows_ncols)
  # plot = nrows*100 + ncols*10 + 1
  grid = AxesGrid(fig, 111, 
                     nrows_ncols=(nrows, ncols), 
                     axes_pad=1.0,
                     share_all=False,
                     cbar_mode='each', 
                     cbar_location='right', 
                     cbar_pad=0.2 )
  for i in range(0,nrows):
    # Loop over columns
    for j in range(0,ncols):
      im = grid[arg].pcolormesh(x[arg], y[arg], zs[arg], cmap=prm.colormap, vmin=zsmin[arg], vmax=zsmax[arg],norm=MidpointNormalize(vmin=zsmin[arg], vmax=zsmax[arg], midpoint=0), rasterized=True)
      # levels = np.array([-0.55,-0.23,0.23,0.55])
      # im2 = grid[arg].contour(x[arg], y[arg], zs[arg], levels, colors='#A9A9A9', linestyles='-', linewidths=1.0)

      grid[arg].set_xticks( np.arange(x[arg].min(), x[arg].max()+0.0001, 90) )
      # ax.xaxis.labelpad = -1
      grid[arg].set_ylim( 0.0, prm.ymax )
      grid[arg].set_aspect(np.diff(grid[arg].get_xlim())/np.diff(grid[arg].get_ylim()))
      if j == 0:
        grid[arg].set_ylabel(ylabels[arg])
      if i == 0:
        grid[arg].set_title(titles[arg], size=prm.titlesize)
      grid[arg].set_xlabel(xlabels[arg], labelpad=-0.05)
      for axis in ['top','bottom','left','right']:
        grid[arg].spines[axis].set_linewidth(prm.linewidth)
      grid[arg].tick_params(axis='x', colors='black',width=prm.linewidth)
      grid[arg].tick_params(axis='y', colors='black',width=prm.linewidth)
      # Add letters to each plot:
      grid[arg].text(0.0, 1.03*prm.ymax, letters[arg])


      cb = grid.cbar_axes[arg].colorbar(im)
      grid.cbar_axes[arg].tick_params(width=2,colors='black')
      grid.cbar_axes[arg].set_ylabel(clabels[arg], size=prm.titlesize)
      grid.cbar_axes[arg].ticklabel_format(style='sci', scilimits=(0,0))
      grid.cbar_axes[arg].yaxis.set_offset_position('left')
      cb.solids.set_rasterized(True) 
      for axis in ['top','bottom','left','right']:
          grid.cbar_axes[arg].spines[axis].set_linewidth(prm.linewidth)

      # Next argument
      arg = arg + 1

  # plt.tight_layout()
  fig.savefig(filename,transparent=True,dpi=prm.fig_dpi, bbox_inches='tight')
  plt.clf()
  return

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
