from PyQt5.QtWidgets import (
    QDialog, QTabWidget, QVBoxLayout, QFormLayout, QComboBox,
    QPushButton, QLabel, QDialogButtonBox, QCheckBox, QSpinBox
)
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QWidget
from ..visualizations import plot_scatter

class ScatterPlotDialog(QDialog):
    def __init__(self, df, canvas):
        super().__init__()
        self.df = df
        self.canvas = canvas
        self.setWindowTitle('Scatter Plot Settings')

        # Create tabbed layout
        self.tabs = QTabWidget()

        general_tab = self._create_general_tab()
        self.tabs.addTab(general_tab, "General")

        aesthetics_tab = self._create_aesthetics_tab()
        self.tabs.addTab(aesthetics_tab, "Aesthetics")

        advanced_tab = self._create_advanced_tab()
        self.tabs.addTab(advanced_tab, "Advanced")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        # Buttons for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.plot_scatter)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def _create_general_tab(self):
        """Create the general tab for scatter plot settings."""
        general_tab = QWidget()
        general_layout = QFormLayout()

        self.x_combo = QComboBox(self)
        self.x_combo.addItems(self.df.columns)
        general_layout.addRow("Select X column:", self.x_combo)

        self.y_combo = QComboBox(self)
        self.y_combo.addItems(self.df.columns)
        general_layout.addRow("Select Y column:", self.y_combo)

        general_tab.setLayout(general_layout)
        return general_tab

    def _create_aesthetics_tab(self):
        """Create the aesthetics tab for scatter plot settings."""
        aesthetics_tab = QWidget()
        aesthetics_layout = QFormLayout()

        self.marker_combo = QComboBox(self)
        self.marker_combo.addItems(['o', 's', 'x', '^', 'D'])
        aesthetics_layout.addRow("Marker Style:", self.marker_combo)

        self.marker_size_spinbox = QSpinBox(self)
        self.marker_size_spinbox.setRange(1, 100)
        self.marker_size_spinbox.setValue(10)
        aesthetics_layout.addRow("Marker Size:", self.marker_size_spinbox)

        self.color_button = QPushButton('Select Color')
        self.color_label = QLabel('')
        self.color_button.clicked.connect(self.select_color)
        aesthetics_layout.addRow("Marker Color:", self.color_button)
        aesthetics_layout.addRow("", self.color_label)

        self.gridlines_checkbox = QCheckBox('Show Gridlines')
        aesthetics_layout.addRow(self.gridlines_checkbox)

        aesthetics_tab.setLayout(aesthetics_layout)
        return aesthetics_tab

    def _create_advanced_tab(self):
        """Create the advanced tab for scatter plot settings."""
        advanced_tab = QWidget()
        advanced_layout = QFormLayout()

        self.trendline_checkbox = QCheckBox('Add Trend Line')
        advanced_layout.addRow(self.trendline_checkbox)

        self.logscale_checkbox = QCheckBox('Logarithmic Scale')
        advanced_layout.addRow(self.logscale_checkbox)

        self.errorbar_checkbox = QCheckBox('Add Error Bars')
        advanced_layout.addRow(self.errorbar_checkbox)

        advanced_tab.setLayout(advanced_layout)
        return advanced_tab

    def select_color(self):
        """Open a color picker dialog to select color."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_label.setText(color.name())
            print(f"Selected color: {color.name()}")

    def plot_scatter(self):
        """Plot the scatter plot based on user settings."""
        x_column = self.x_combo.currentText()
        y_column = self.y_combo.currentText()
        marker = self.marker_combo.currentText()
        marker_size = self.marker_size_spinbox.value()
        color = self.color_label.text() if self.color_label.text() else None
        add_trendline = self.trendline_checkbox.isChecked()
        logscale = self.logscale_checkbox.isChecked()
        error_bars = self.errorbar_checkbox.isChecked()
        show_gridlines = self.gridlines_checkbox.isChecked()

        # Clear previous plot
        self.canvas.figure.clear()

        # Call the plot function from visualizations
        plot_scatter(
            fig=self.canvas.figure,
            df=self.df[[x_column, y_column]],
            marker=marker,
            marker_size=marker_size,
            color=color,
            log_scale=logscale,
            add_trendline=add_trendline,
            error_bars=error_bars,
            gridlines=show_gridlines
        )
        self.canvas.draw()

        print(f"Scatter plot created with X: {x_column}, Y: {y_column}, "
              f"Marker: {marker}, Size: {marker_size}, Color: {color}, "
              f"Gridlines: {show_gridlines}")
        self.accept()

