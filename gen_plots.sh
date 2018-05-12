#!/bin/sh

source ~/.local/share/virtualenvs/matplotlib2tikz-LEw3aJtk/bin/activate

for f in plot_*.py
do
    MPLBACKEND=Qt5Agg python $f
done

