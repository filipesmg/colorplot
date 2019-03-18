import numpy as np                            # Numerical library
import sys                                    # System library (to read arguments from command line)

################################################################################
# Build the local frame:
#  m x \delta s  ,  m x (m x \delta s)  ,  m 
################################################################################
def build_local_frame(mtheta,mphi,deltas):
  mtheta *= np.pi
  mphi   *= np.pi
  m = np.array([ np.sin(mtheta)*np.cos(mphi) , np.sin(mtheta)*np.sin(mphi) , np.cos(mtheta)])
  mxdeltas   = np.cross(m,deltas)
  mxmxdeltas = np.cross(m,mxdeltas)
  return mxdeltas, mxmxdeltas, m

################################################################################
# Build the spherical frame:
#  \theta  ,  \phi  ,  r
################################################################################
def build_spherical_frame(mtheta,mphi):
  mtheta *= np.pi
  mphi   *= np.pi
  e_theta = ( np.cos(mtheta)*np.cos(mphi) , np.cos(mtheta)*np.sin(mphi) , -np.sin(mtheta) ) # theta
  e_phi   = (               -np.sin(mphi) ,                np.cos(mphi) ,      0.0        ) # phi
  e_r     = ( np.sin(mtheta)*np.cos(mphi) , np.sin(mtheta)*np.sin(mphi) ,  np.cos(mtheta) ) # r
  return e_theta, e_phi, e_r


################################################################################
# Transform :
#  m x \delta s  ,  m x (m x \delta s)  ,  m 
#
#  m        is given through theta and phi in columns 4 and 5 of values_global
#  deltas   is received as an argument 
################################################################################
def global_to_local(values_global,deltas,frame):
  values_local = [ [] for _ in range(3) ]
  for line_x,line_y,line_z in zip(values_global[0],values_global[1],values_global[2]):
    if (not (line_x[0] == line_y[0] == line_z[0])) or (not (line_x[1] == line_y[1] == line_z[1])) or (not (line_x[-2] == line_y[-2] == line_z[-2])) or (not (line_x[-1] == line_y[-1] == line_z[-1])):
      print("Magnetization direction is not the same for all the inputs")
      sys.exit(0)

    if line_x[-2]<=1.0 and line_x[-1]<=1.0:
      vec_real = ( line_x[2] , line_y[2] , line_z[2] )
      vec_imag = ( line_x[3] , line_y[3] , line_z[3] )
    elif line_x[-2]>1.0 and line_x[-1]<1.0:
      vec_real = ( line_x[2] , line_y[2] , -line_z[2] )
      vec_imag = ( line_x[3] , line_y[3] , -line_z[3] )
    elif line_x[-2]<1.0 and line_x[-1]>1.0:
      vec_real = ( line_x[2] , -line_y[2] , -line_z[2] )
      vec_imag = ( line_x[3] , -line_y[3] , -line_z[3] )
    else:
      print "NOT IMPLEMENTED ANGLES"
      sys.exit()

    if frame == "local":
      xp,yp,zp = build_local_frame(line_x[-2],line_x[-1],deltas)
    elif frame == "spherical":
      if (line_x[-2] == 0.0) or (line_x[-2] == 1.0) or (line_x[-2] == 2.0): # Skip poles where theta and phi directions are not defined
        continue
      xp,yp,zp = build_spherical_frame(line_x[-2],line_x[-1])
    else:
      xp = (1.0,0.0,0.0)
      yp = (0.0,1.0,0.0)
      zp = (0.0,0.0,1.0)

    field_like_real  = np.dot(vec_real,xp)
    damp_like_real   = np.dot(vec_real,yp)
    longitud_real    = np.dot(vec_real,zp)
    field_like_imag  = np.dot(vec_imag,xp)
    damp_like_imag   = np.dot(vec_imag,yp)
    longitud_imag    = np.dot(vec_imag,zp)
    field_like_amp   = np.sqrt((field_like_real)**2 + (field_like_imag)**2 )
    damp_like_amp    = np.sqrt((damp_like_real)**2 + (damp_like_imag)**2 )  
    longitud_amp     = np.sqrt((longitud_real)**2 +  (longitud_imag)**2 )   
    field_like_phase = np.arctan2(field_like_real,field_like_imag)
    damp_like_phase  = np.arctan2(damp_like_real,damp_like_imag)  
    longitud_phase   = np.arctan2(longitud_real,longitud_imag)    

    values_local[0].append( (line_x[0], line_x[1], field_like_real, field_like_imag, field_like_amp , field_like_phase , line_x[-2] , line_x[-1] ) )
    values_local[1].append( (line_x[0], line_x[1], damp_like_real , damp_like_imag , damp_like_amp  , damp_like_phase  , line_x[-2] , line_x[-1] ) )
    values_local[2].append( (line_x[0], line_x[1], longitud_real  , longitud_imag  , longitud_amp   , longitud_phase   , line_x[-2] , line_x[-1] ) )
  return values_local