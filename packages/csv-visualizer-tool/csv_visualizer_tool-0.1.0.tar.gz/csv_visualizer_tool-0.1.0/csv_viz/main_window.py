import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QFileDialog, QDialog, QTableWidget, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
from csv_viz.plot_settings.scatter_plot_dialog import ScatterPlotDialog
from csv_viz.plot_settings.boxplot_dialog import BoxPlotDialog
from csv_viz.plot_settings.heatmap_dialog import HeatmapDialog
from csv_viz.plot_settings.violin_plot_dialog import ViolinPlotDialog
from csv_viz.plot_settings.pairplot_dialog import PairPlotDialog
from csv_viz.plot_settings.catplot_dialog import CatPlotDialog
from csv_viz.plot_settings.error_bars_plot_dialog import ErrorBarsPlotDialog
from csv_viz.plot_settings.trendline_plot_dialog import TrendlinePlotDialog
from csv_viz.plot_settings.multiple_data_plot_dialog import MultipleDataPlotDialog
from csv_viz.plot_settings.histogram_plot_dialog import HistogramPlotDialog
from csv_viz.data_operations import DataOperationsDialog
from csv_viz.utils import load_csv, export_filtered_data


class CSVVizApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.df = None
        self.filtered_df = None  # Store filtered data

        self.setWindowTitle("CSV Visualizer with Seaborn")
        self.setGeometry(100, 100, 1200, 800)

        # Set up the layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Set up sections
        self._create_file_section()
        self._create_plotting_section()

        # Canvas for plotting
        self.canvas = FigureCanvas(Figure(figsize=(7, 5)))
        self.toolbar = NavigationToolbar2QT(self.canvas, self)  # Add Matplotlib toolbar
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def _create_file_section(self):
        """File operations section: Load CSV, view data, view stats"""
        self.load_csv_button = QPushButton('Load CSV', self)
        self.load_csv_button.clicked.connect(self.load_csv_file)
        self.layout.addWidget(self.load_csv_button)

        self.view_csv_button = QPushButton('View CSV Data', self)
        self.view_csv_button.clicked.connect(self.view_csv_data)
        self.view_csv_button.setEnabled(False)
        self.layout.addWidget(self.view_csv_button)

        self.stats_button = QPushButton('View Statistics', self)
        self.stats_button.clicked.connect(self.view_statistics)
        self.stats_button.setEnabled(False)
        self.layout.addWidget(self.stats_button)

        # Data operations
        self.data_operations_button = QPushButton('Data Operations', self)
        self.data_operations_button.clicked.connect(self.open_data_operations)
        self.layout.addWidget(self.data_operations_button)

    def _create_plotting_section(self):
        """Plotting options section: Select plot type and plot"""
        self.plot_type_combo = QComboBox(self)
        self.plot_type_combo.addItems(['Scatter', 'Boxplot', 'Heatmap', 'Violin', 'Trend Line', 
                                       'Multiple Data', 'Histogram', 'Pairplot', 'Catplot'])
        self.layout.addWidget(self.plot_type_combo)

        self.plot_button = QPushButton('Plot Data', self)
        self.plot_button.clicked.connect(self.open_plot_settings)
        self.plot_button.setEnabled(False)
        self.layout.addWidget(self.plot_button)

    def load_csv_file(self):
        """Load CSV file"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            self.df = load_csv(file_name)
            if self.df is not None:
                self.filtered_df = self.df
                self.view_csv_button.setEnabled(True)
                self.stats_button.setEnabled(True)
                self.plot_button.setEnabled(True)

    def open_plot_settings(self):
        """Open plot settings based on the selected plot type"""
        plot_type = self.plot_type_combo.currentText()
        if plot_type == 'Scatter':
            dialog = ScatterPlotDialog(self.df, self.canvas)
        elif plot_type == 'Boxplot':
            dialog = BoxPlotDialog(self.df, self.canvas)
        elif plot_type == 'Heatmap':
            dialog = HeatmapDialog(self.df, self.canvas)
        elif plot_type == 'Violin':
            dialog = ViolinPlotDialog(self.df, self.canvas)
        elif plot_type == 'Trend Line':
            dialog = TrendlinePlotDialog(self.df, self.canvas)
        elif plot_type == 'Multiple Data':
            dialog = MultipleDataPlotDialog(self.df, self.canvas)
        elif plot_type == 'Histogram':
            dialog = HistogramPlotDialog(self.df, self.canvas)
        elif plot_type == 'Pairplot':
            dialog = PairPlotDialog(self.df, self.canvas)
        elif plot_type == 'Catplot':
            dialog = CatPlotDialog(self.df, self.canvas)
        # Add other plot dialogs as needed
        dialog.exec_()

    def open_data_operations(self):
        """Open data operations dialog and export the data if modified"""
        dialog = DataOperationsDialog(self.df)
        dialog.exec_()

        # Export the modified data after operations
        if dialog.filtered_df is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Filtered Data", "", "CSV Files (*.csv)")
            if file_name:
                export_filtered_data(dialog.filtered_df, file_name)

    def view_csv_data(self):
        """Open a dialog to view the loaded CSV data."""
        if self.filtered_df is not None:
            dialog = ViewCSVDataDialog(self.filtered_df)
            dialog.exec_()

    def view_statistics(self):
        """Open a dialog to view the CSV data statistics."""
        if self.filtered_df is not None:
            dialog = ViewCSVStatsDialog(self.filtered_df)
            dialog.exec_()


class ViewCSVDataDialog(QDialog):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setWindowTitle('CSV Data Viewer')
        self.resize(800, 800)

        layout = QVBoxLayout()

        # Create a table to display CSV data
        table_widget = QTableWidget()
        table_widget.setRowCount(len(self.df))
        table_widget.setColumnCount(len(self.df.columns))
        table_widget.setHorizontalHeaderLabels(self.df.columns)

        # Populate the table with CSV data
        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                table_widget.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))

        layout.addWidget(table_widget)
        self.setLayout(layout)

    def exec_(self):
        """Run the dialog."""
        super().exec_()


class ViewCSVStatsDialog(QDialog):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.setWindowTitle('CSV Statistics Viewer')
        self.resize(800, 800)

        layout = QVBoxLayout()

        # Get the statistics using df.describe()
        stats = self.df.describe()

        # Create a table to display CSV statistics
        table_widget = QTableWidget()
        table_widget.setRowCount(len(stats))
        table_widget.setColumnCount(len(stats.columns))
        table_widget.setHorizontalHeaderLabels(stats.columns)
        table_widget.setVerticalHeaderLabels(stats.index)

        # Populate the table with statistics
        for i in range(len(stats)):
            for j in range(len(stats.columns)):
                table_widget.setItem(i, j, QTableWidgetItem(str(stats.iat[i, j])))
                
        layout.addWidget(table_widget)
        self.setLayout(layout)

    def exec_(self):
        """Run the dialog."""
        super().exec_()


def run_app():
    """Entry point for the application."""
    app = QApplication(sys.argv)
    main_window = CSVVizApp()  # Assuming CSVVizApp is your main window class
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()

