import numpy as np                            # Numerical library
from cycler import cycler
import matplotlib.pyplot as plt               # Plotting library
from string import ascii_lowercase
import parameters as prm
import fit_spherical as fit

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
  for l in range( nfigs ): # Number of figures (real, imag, etc.)
    fig, axs = plt.subplots(1, ncols, figsize=(9, 3), sharey=False)
    for j in range( ncols ): # Number of columns in each figure (different components: x,y,z or theta,phi,r or mxs,mx(mxs),m)
      axs[j].set_prop_cycle( custom_cycler )
      for i in range( len(y[l][j]) ): # Number of curves (different rotations z->x, z->y, x->y for all cuts)
        if prm.output_prefix == 'Beff_spherical_w' and l == 1 and i != 2: # Fit imaginary part of effective field for z->x, z->y
          if j == 0: # theta component
            if i == 0: # z -> y (FeW, which is equivalent to z->x, where x is the direction of the E field)
              popt, pcov = fit.curve_fit(fit.b_theta_phi0 , x[l][j][i], y[l][j][i])
              for e in range( len(x[l][j][i]) ):
                y[l][j][i][e] = fit.b_theta_phi0(x[l][j][i][e], popt[0], popt[1], popt[2])
            if i == 1: # z -> x (FeW, which is equivalent to z->y, where y is the direction of \delta s)
              popt, pcov = fit.curve_fit(fit.b_theta_phi90, x[l][j][i], y[l][j][i])
              for e in range( len(x[l][j][i]) ):
                y[l][j][i][e] = fit.b_theta_phi90(x[l][j][i][e], popt[0], popt[1], popt[2])
          if j == 1: # phi component
            if i == 0: # z -> y (FeW, which is equivalent to z->x, where x is the direction of the E field)
              popt, pcov = fit.curve_fit(fit.b_phi_phi0 , x[l][j][i], y[l][j][i])
              for e in range( len(x[l][j][i]) ):
                y[l][j][i][e] = fit.b_phi_phi0(x[l][j][i][e], popt[0], popt[1], popt[2])
            if i == 1: # z -> x (FeW, which is equivalent to z->y, where y is the direction of \delta s)
              popt, pcov = fit.curve_fit(fit.b_phi_phi90, x[l][j][i], y[l][j][i])
              for e in range( len(x[l][j][i]) ):
                y[l][j][i][e] = fit.b_phi_phi90(x[l][j][i][e], popt[0], popt[1], popt[2])
          if j == 2: # r component
            if i == 0: # z -> y (FeW, which is equivalent to z->x, where x is the direction of the E field)
              popt, pcov = fit.curve_fit(fit.b_r_phi0 , x[l][j][i], y[l][j][i])
              for e in range( len(x[l][j][i]) ):
                y[l][j][i][e] = fit.b_r_phi0(x[l][j][i][e], popt[0], popt[1], popt[2])
            if i == 1: # z -> x (FeW, which is equivalent to z->y, where y is the direction of \delta s)
              popt, pcov = fit.curve_fit(fit.b_r_phi90, x[l][j][i], y[l][j][i])
              for e in range( len(x[l][j][i]) ):
                y[l][j][i][e] = fit.b_r_phi90(x[l][j][i][e], popt[0], popt[1], popt[2])
          print j,i,popt
        axs[j].plot( x[l][j][i],y[l][j][i] )

      axs[j].axhline(y=0, linestyle='-', linewidth=1.0, color='k')
      for axis in ['top','bottom','left','right']:
        axs[j].spines[axis].set_linewidth(prm.linewidth)
      # axs[j].text(0.0, 1.03*np.array(y[l][j][i]).max(), letters[j])
      # axs[j].set_title(prm.clabel[j], size=prm.titlesize, pad=15)
      axs[j].set_ylabel(prm.clabel_local[j] if prm.frame == "local" else prm.clabel_cartesian[j] if prm.frame == "cartesian" else prm.clabel_spherical[j])
      axs[j].set_xlabel(r'Magnetization angle (degrees)')
      # axs[j].set_xlim(np.array(x[l][0][0]).min(),np.array(x[l][0][0]).max())
      # axs[j].set_xticks( np.arange(np.array(x[l][0][0]).min(), np.array(x[l][0][0]).max()+0.0001, 90) )
      axs[j].set_xlim(0.0,360.0 if prm.double_angles else 180.0 )
      axs[j].set_xticks( np.arange(0.0, 360.0001 if prm.double_angles else 180.0001, 90) )
      axs[j].tick_params(axis='x', colors='black',width=prm.linewidth)
      axs[j].tick_params(axis='y', colors='black',width=prm.linewidth)
      axs[j].ticklabel_format(axis='y',style='sci', scilimits=(0,0))

    plt.tight_layout()
    plt.savefig(prm.output_prefix+'_cut_'+prm.stype[l]+'.pdf',transparent=True,dpi=prm.fig_dpi, bbox_inches='tight')
    plt.clf()

  # Custom cut: in this case, damping-like field:
  comp=2
  prefix=['_fl_','_dl_','_lg_']
  for l in range( nfigs ):
    fig, axs = plt.subplots(2, 1, figsize=(6, 6), sharey=False)
    # for i in range( len(y[l][1]) ):
    #   print i,len(y[l][1]),i//2,i%2
    axs[0].set_prop_cycle( cycler(color=prm.colors) * cycler(ls=['solid']) )
    axs[0].set_title('Static limit (dc)', size=prm.titlesize, pad=15)
    axs[1].set_prop_cycle( cycler(color=prm.colors) * cycler(ls=['dashed']) )
    axs[1].set_title('Resonance (ac)', size=prm.titlesize, pad=15)
    for i in range( len(y[l][comp]) ):
      i0 = i%2
      
      axs[i0].plot( x[l][comp][i],y[l][comp][i] )

      for axis in ['top','bottom','left','right']:
        axs[i0].spines[axis].set_linewidth(prm.linewidth)
      # axs[i].text(0.0, 1.03*np.array(y[l][j][i]).max(), letters[j])
      # axs[i].set_title(prm.clabel_local[j] if prm.local else prm.clabel_global[j], size=prm.titlesize, pad=15)
      axs[i0].set_ylabel(prm.clabel_local[comp] if prm.frame == "local" else prm.clabel_cartesian[comp] if prm.frame == "cartesian" else prm.clabel_spherical[comp])
      axs[i0].set_xlabel(r'Magnetization angle (degrees)', labelpad=-0.1)
      axs[i0].set_xlim(np.array(x[l][comp][0]).min(),np.array(x[l][comp][0]).max())
      axs[i0].set_xticks( np.arange(np.array(x[l][comp][0]).min(), np.array(x[l][comp][0]).max()+0.0001, 90) )
      axs[i0].tick_params(axis='x', colors='black',width=prm.linewidth)
      axs[i0].tick_params(axis='y', colors='black',width=prm.linewidth)
      axs[i0].ticklabel_format(axis='y',style='sci', scilimits=(0,0))

    plt.tight_layout()
    plt.savefig(prm.output_prefix+'_cut'+prefix[comp]+prm.stype[l]+'.pdf',transparent=True,dpi=prm.fig_dpi, bbox_inches='tight')


  return