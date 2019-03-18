import numpy as np                            # Numerical library
from   scipy.optimize import curve_fit

################################################################################
# Defining functional forms for spherical components of effective fields
################################################################################
def b_theta_phi0(theta, ap0, ap2, ap4):
    return  ap0 + ap2*(np.sin(theta*np.pi/180.0)**2) + ap4*(np.sin(theta*np.pi/180.0)**4)

def b_theta_phi90(theta, at0, bp2, bp4):
    return  np.cos(theta*np.pi/180.0)*(-at0 + bp2*(np.sin(theta*np.pi/180.0)**2) + bp4*(np.sin(theta*np.pi/180.0)**4))

def b_phi_phi0(theta, at0, at2, at4):
    return  -(at0 + at2*(np.sin(theta*np.pi/180.0)**2) + at4*(np.sin(theta*np.pi/180.0)**4))

def b_phi_phi90(theta, ap0, bt2, bt4):
    return  -np.cos(theta*np.pi/180.0)*(ap0 + bt2*(np.sin(theta*np.pi/180.0)**2) + bt4*(np.sin(theta*np.pi/180.0)**4))

def b_r_phi0(theta, ar0, ar2, ar4):
    return  np.sin(theta*np.pi/180.0)*np.cos(theta*np.pi/180.0)*(ar0 + ar2*(np.sin(theta*np.pi/180.0)**2) + ar4*(np.sin(theta*np.pi/180.0)**4))

def b_r_phi90(theta, br0, br2, br4):
    return  np.sin(theta*np.pi/180.0)*(br0 + br2*(np.sin(theta*np.pi/180.0)**2) + br4*(np.sin(theta*np.pi/180.0)**4))

