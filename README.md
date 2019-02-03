# colorplot
Python script to plot colormaps in global and local frame of reference, and its cuts.

Use as:

`ipython ${folder}/colorplot_localframe.py 'filenames_x' 'filenames_y' 'filenames_z' (...)`

where 'filenames_α' includes the α-component of the quantity to be plotted. E.g.:
ipython ~/programs/scripts/colorplot.py results/TSOC/5Npl/SOT/SOTx results/TSOC/5Npl/SOT/SOTy results/TSOC/5Npl/SOT/SOTz

* The number of arguments gives the number of graphs plotted.
* Wildcards can be used inside quotation marks.
* Options are set inside `parameters.py`.
