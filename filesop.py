import glob                                   # Unix style pathname pattern expansion
import re                                     # Regular expression operators
import pandas as pd                           # Python Data Analysis Library
import numpy as np                            # Numerical library
from parameters import prefactor_frequency

################################################################################
# Get all files in the input path(s)
################################################################################
def get_filenames(path):
  # glob return a list with all the files listed by path
  files = glob.glob(path+'*')
  return files

################################################################################
# Get the values of the field from the filename
################################################################################
def get_field_from_name(file):
  hwa = re.compile("hwa=( ){0,}([0-9]){1,}.([0-9]){1,}E[+-]([0-9]){1,}")
  hwt = re.compile("hwt=( ){0,}([0-9]){1,}.([0-9]){1,}")
  hwp = re.compile("hwp=( ){0,}([0-9]){1,}.([0-9]){1,}")
  m1 = hwa.search(file)
  m2 = hwt.search(file)
  m3 = hwp.search(file)
  if(m1 == None or m2 == None or m3 == None):
    return (0.0,0.0,0.0)
  str = m1.group(0)
  a = float(str[4:])
  str = m2.group(0)
  t = float(str[4:])
  str = m3.group(0)
  p = float(str[4:])
  return (a,t,p)

################################################################################
# Get the data from the file and save it into a matrix
################################################################################
def read_data_from_file(file):
  # Reading the data from the file
  data = pd.read_csv(file,
                    skiprows=1,
                    header=None,
                    delim_whitespace=True,
                    usecols=[0,1,2,3,4,5,6]).values
  ndata = np.array(data[:, [0, 2, 3]])
  return ndata

################################################################################
# Read the magnetization direction from file (in units of pi radians)
################################################################################
def get_magnetization_direction(file):
  # Reading the data from the file
  data = pd.read_csv(file,
                    skiprows=1,
                    nrows=1,
                    header=None,
                    delim_whitespace=True,
                    usecols=[7,8]).values
  if len(data) < 1:
    mtheta , mphi = 0.0 , 0.0
    success = False
  else:
    ndata = np.array(data)
    mtheta , mphi = ndata[0][0] , ndata[0][1]
    success = True
  return [ mtheta, mphi ], success

################################################################################
# Get the desired values from the files
################################################################################
def get_values(field_component,files,double_angles):
  # Loop over the files in each argument
  values = []
  mangle = []
  files.sort()
  for filename in files:
    # Get the value of the field from the filename
    field = get_field_from_name(filename)
    # Get the magnetization direction from file
    mangle, success = get_magnetization_direction(filename)
    if not success:
      continue
    # Get the required data from the file
    ndata = read_data_from_file(filename)
    # Building the two-dimension variable to be plotted
    for line in ndata:
      if prefactor_frequency: 
        prefactor = 1.0/line[0]
      else:
        prefactor = 1.0
      # Transforming angles to degree and frequency to THz
      # As a function of the field angle:
      # values.append( ( field[field_component]*180 , line[0]*13.6*1000/4.135667 , line[1] , line[2] ,  mangle[0] , mangle[1] ) )
      # As a function of the magnetization angle:
      values.append( ( mangle[field_component-1]*180 , line[0]*13.6*1000/4.135667 , line[1]*prefactor , -line[2]*prefactor ,  mangle[0] , mangle[1] ) )
      # values.append( ( field[field_component]*180 , line[0]*13.6*1000/4.135667 , line[1] , line[2] ,  field[1] , field[2] ) )
      if (double_angles==True) and (field[field_component] != 1.0):
        # As a function of the field angle:
        # values.append( ( (2.0-field[field_component])*180 , line[0]*13.6*1000/4.135667 , line[1] , line[2] , (-2*field_component+4)+(2*field_component-3)*mangle[0] , (2*field_component-2)+(-2*field_component+3)*mangle[1] ) )
        # As a function of the magnetization angle:
        add_line = ( (2.0-mangle[field_component-1])*180 , line[0]*13.6*1000/4.135667 , line[1]*prefactor , -line[2]*prefactor , (-2*field_component+4)+(2*field_component-3)*mangle[0] , (2*field_component-2)+(-2*field_component+3)*mangle[1] )
        # values.append( ( (2.0-field[field_component])*180 , line[0]*13.6*1000/4.135667 , line[1] , line[2] , (-2*field_component+4)+(2*field_component-3)*field[1] , (2*field_component-2)+(-2*field_component+3)*field[2] ) )
        values.append( add_line )
  return values






