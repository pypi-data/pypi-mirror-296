print('''
This is a plotting module to plot the output of the scanner package.
There are three types of plotting: 
   1) scatter plot for 2 d. This can be used via plot_scatter_2d() function
   2) scatter plot for 3 d. This can be used via plot_scatter_3d() function
   3) plot histogram of one or more output. This can be ised vis plot_hist() function
''')


import matplotlib.pyplot as plt 
import numpy as np

def plot_scatter_2d(in_:str, col1,col2):
  x = np.loadtxt(in_,delimiter=',')
  l = open(in_,'r')
  n = l.readlines()[0]
  n = n.split('')
  labels = [i for i in n if i != '#'] 
