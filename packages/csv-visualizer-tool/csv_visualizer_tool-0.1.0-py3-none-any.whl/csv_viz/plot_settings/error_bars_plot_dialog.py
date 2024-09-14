from PyQt5.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QFormLayout, QComboBox, QPushButton, QLabel, QDialogButtonBox, QCheckBox
from PyQt5.QtWidgets import QColorDialog
from ..visualizations import plot_with_error_bars
from PyQt5.QtWidgets import QWidget


class ErrorBarsPlotDialog(QDialog):
    def __init__(self, df, canvas):
        super().__init__()
        self.df = df
        self.canvas = canvas
        self.setWindowTitle('Error Bars Plot Settings')

        # Create tabbed layout
        self.tabs = QTabWidget()

        general_tab = self._create_general_tab()
        self.tabs.addTab(general_tab, "General")

        aesthetics_tab = self._create_aesthetics_tab()
        self.tabs.addTab(aesthetics_tab, "Aesthetics")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        # Buttons for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.plot_with_error_bars)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def _create_general_tab(self):
        """Create the general tab for error bars plot settings."""
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
        """Create the aesthetics tab for error bars plot settings."""
        aesthetics_tab = QWidget()
        aesthetics_layout = QFormLayout()

        self.marker_combo = QComboBox(self)
        self.marker_combo.addItems(['o', 's', 'x', '^', 'D'])
        aesthetics_layout.addRow("Marker Style:", self.marker_combo)

        self.color_button = QPushButton('Select Color')
        self.color_label = QLabel('')
        self.color_button.clicked.connect(self.select_color)
        aesthetics_layout.addRow("Marker Color:", self.color_button)
        aesthetics_layout.addRow("", self.color_label)

        self.logscale_checkbox = QCheckBox('Logarithmic Scale')
        aesthetics_layout.addRow(self.logscale_checkbox)

        aesthetics_tab.setLayout(aesthetics_layout)
        return aesthetics_tab

    def select_color(self):
        """Open a color picker dialog to select color."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_label.setText(color.name())

    def plot_with_error_bars(self):
        """Plot the plot with error bars based on user settings."""
        x_column = self.x_combo.currentText()
        y_column = self.y_combo.currentText()
        marker = self.marker_combo.currentText()
        color = self.color_label.text() if self.color_label.text() else None
        logscale = self.logscale_checkbox.isChecked()

        # Clear previous plot
        self.canvas.figure.clear()

        # Call the plot function from visualizations
        plot_with_error_bars(self.canvas.figure, self.df[[x_column, y_column]], marker=marker, color=color, log_scale=logscale)
        self.canvas.draw()

        print(f"Error bars plot created with X: {x_column}, Y: {y_column}, Marker: {marker}, Color: {color}")
        self.accept()

