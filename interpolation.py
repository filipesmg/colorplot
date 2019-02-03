import numpy as np                            # Numerical library
import scipy.interpolate                      # Interpolation library

################################################################################
# Interpolate the values
################################################################################
def interpolate(values):
  # Sorting values
  values.sort()

  # Separating the values for the fit
  x = np.array([v[0] for v in values])
  y = np.array([v[1] for v in values])

  # Getting number of points in x and y: nx repetitions of y[0]
  nx = sum(y == y[0])
  ny = len(x)/nx

  # Removing repetitions
  x_orig = x[::ny]
  y_orig = y[:ny]

  z = []
  f = []
  for i in range(len(values[0])-4):
    z.append(np.array([v[i+2] for v in values]))

    z[i].shape = (nx, ny)

    # Interpolation for data on rectangular grids using a bivariate cubic spline
    f.append( scipy.interpolate.RectBivariateSpline(x_orig, y_orig, z[i]) )

    # Getting new interpolated values (tenfold points on each axis, adjust this depending on the input file)
    x = np.linspace(x_orig.min(), x_orig.max(), 10*nx)
    y = np.linspace(y_orig.min(), y_orig.max(), 10*ny)
    z[i] = f[i](x, y).transpose()

  return x, y, z
