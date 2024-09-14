from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QSpinBox, QDialogButtonBox, QCheckBox, QPushButton, QLabel, QColorDialog
from ..visualizations import plot_histogram
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QWidget


class HistogramPlotDialog(QDialog):
    def __init__(self, df, canvas):
        super().__init__()
        self.df = df
        self.canvas = canvas
        self.setWindowTitle('Histogram Settings')

        # Create layout
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.column_combo = QComboBox(self)
        self.column_combo.addItems(self.df.columns)
        form_layout.addRow("Select Column:", self.column_combo)

        self.bins_spinbox = QSpinBox(self)
        self.bins_spinbox.setRange(1, 100)
        self.bins_spinbox.setValue(10)
        form_layout.addRow("Number of Bins:", self.bins_spinbox)

        self.color_button = QPushButton('Select Color')
        self.color_label = QLabel('')
        self.color_button.clicked.connect(self.select_color)
        form_layout.addRow("Bar Color:", self.color_button)
        form_layout.addRow("", self.color_label)

        self.logscale_checkbox = QCheckBox('Logarithmic Scale')
        form_layout.addRow(self.logscale_checkbox)

        layout.addLayout(form_layout)

        # Buttons for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.plot_histogram)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def select_color(self):
        """Open a color picker dialog to select color."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_label.setText(color.name())

    def plot_histogram(self):
        """Plot the histogram based on user settings."""
        column = self.column_combo.currentText()
        bins = self.bins_spinbox.value()
        color = self.color_label.text() if self.color_label.text() else 'blue'
        logscale = self.logscale_checkbox.isChecked()

        # Clear previous plot
        self.canvas.figure.clear()

        # Call the plot function from visualizations
        plot_histogram(self.canvas.figure, self.df[[column]], bins=bins, color=color, log_scale=logscale)
        self.canvas.draw()

        print(f"Histogram created for column: {column}, Bins: {bins}, Color: {color}")
        self.accept()

