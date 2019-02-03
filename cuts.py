import numpy as np                            # Numerical library
from cycler import cycler
import matplotlib.pyplot as plt               # Plotting library
from string import ascii_lowercase
import parameters as prm

################################################################################
# Identify the closest values to 'values' in data[comp]
################################################################################
def get_closest_values(data,comp,values):
  # Loop through the given values
  closest_values = []
  for value in values:
    diff = 999.0
    # Loop through the data to compare with given values
    for line in data:
      diff_new = abs(line[comp] - value)
      # print 'comparison:',line[comp],value,diff_new
      # If new value is closer then previous one, store it
      if (diff_new < diff):
        diff = diff_new
        add_value = line[comp]

    # Adding closest value to the list
    closest_values.append(add_value)
  return closest_values


################################################################################
# Get all the lines with data[comp] = values
# Return a list cuts with len(values) elements, each being a cut wfor the values
# in the list 'values'
################################################################################
def get_cuts(data,comp,values):
  closest_values = get_closest_values(data,comp,values)

  cuts = []
  for value in closest_values:
    cut = []
    for line in data:
      if abs(line[comp] - value) < 1.e-10:
        cut.append(line)
    cut.sort()
    cuts.append(cut)

  return cuts


def plot_cuts( nfigs , ncols , x , y):
  custom_cycler = ( cycler(color=prm.colors) * cycler(ls=prm.linestyles))
  # letters = [(r'\textbf{'+ascii_lowercase[_]+')}') for _ in range(ncols)]
  # ax1.set_prop_cycle(custom_cycler)
  for l in range( nfigs ):
    fig, axs = plt.subplots(1, ncols, figsize=(9, 3), sharey=False)
    for j in range( ncols ):
      axs[j].set_prop_cycle( custom_cycler )
      for i in range( len(y[l][j]) ):
        axs[j].plot( x[l][j][i],y[l][j][i] )

      for axis in ['top','bottom','left','right']:
        axs[j].spines[axis].set_linewidth(prm.linewidth)
      # axs[j].text(0.0, 1.03*np.array(y[l][j][i]).max(), letters[j])
      # axs[j].set_title(prm.clabel[j], size=prm.titlesize, pad=15)
      axs[j].set_ylabel(prm.clabel[j])
      axs[j].set_xlabel(r'Magnetization angle (degrees)')
      axs[j].set_xlim(np.array(x[l][0][0]).min(),np.array(x[l][0][0]).max())
      axs[j].set_xticks( np.arange(np.array(x[l][0][0]).min(), np.array(x[l][0][0]).max()+0.0001, 90) )
      axs[j].tick_params(axis='x', colors='black',width=prm.linewidth)
      axs[j].tick_params(axis='y', colors='black',width=prm.linewidth)
      axs[j].ticklabel_format(axis='y',style='sci', scilimits=(0,0))

    plt.tight_layout()
    plt.savefig(prm.output_prefix+'_cut_'+prm.stype[l]+'.pdf',transparent=True,dpi=prm.fig_dpi, bbox_inches='tight')
    plt.clf()
  return