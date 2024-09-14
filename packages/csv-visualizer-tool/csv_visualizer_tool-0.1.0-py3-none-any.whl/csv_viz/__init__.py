# csv_viz/__init__.py

# Import the main modules so they can be accessed directly from the csv_viz package
from .main_window import CSVVizApp
from .data_operations import DataOperationsDialog
from .utils import load_csv
from .visualizations import (
    plot_scatter, plot_boxplot, plot_heatmap, plot_violin, plot_trendline,
    plot_with_error_bars, plot_multiple, plot_histogram
)

# Import the plot dialogs from plot_settings
from .plot_settings.scatter_plot_dialog import ScatterPlotDialog
from .plot_settings.boxplot_dialog import BoxPlotDialog
from .plot_settings.heatmap_dialog import HeatmapDialog
from .plot_settings.violin_plot_dialog import ViolinPlotDialog
from .plot_settings.pairplot_dialog import PairPlotDialog
from .plot_settings.catplot_dialog import CatPlotDialog

