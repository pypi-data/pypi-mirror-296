from PyQt5.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QFormLayout, QComboBox, QPushButton, QLabel, QDialogButtonBox, QListWidget, QCheckBox
from PyQt5.QtWidgets import QColorDialog
from ..visualizations import plot_multiple
from PyQt5.QtWidgets import QWidget


class MultipleDataPlotDialog(QDialog):
    def __init__(self, df_list, canvas, labels):
        super().__init__()
        self.df_list = df_list
        self.canvas = canvas
        self.labels = labels
        self.setWindowTitle('Multiple Data Plot Settings')

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
        button_box.accepted.connect(self.plot_multiple)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def _create_general_tab(self):
        """Create the general tab for multiple data plot settings."""
        general_tab = QWidget()
        general_layout = QFormLayout()

        self.data_list = QListWidget(self)
        self.data_list.addItems(self.labels)
        general_layout.addRow("Select Data Sets:", self.data_list)

        general_tab.setLayout(general_layout)
        return general_tab

    def _create_aesthetics_tab(self):
        """Create the aesthetics tab for multiple data plot settings."""
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

    def plot_multiple(self):
        """Plot the multiple data plot based on user settings."""
        selected_datasets = [self.df_list[i] for i in range(self.data_list.count()) if self.data_list.isItemSelected(self.data_list.item(i))]
        selected_labels = [self.labels[i] for i in range(self.data_list.count()) if self.data_list.isItemSelected(self.data_list.item(i))]
        
        marker = self.marker_combo.currentText()
        color = self.color_label.text() if self.color_label.text() else None
        logscale = self.logscale_checkbox.isChecked()

        # Clear previous plot
        self.canvas.figure.clear()

        # Call the plot function from visualizations
        plot_multiple(self.canvas.figure, selected_datasets, selected_labels, marker=marker, color=color, log_scale=logscale)
        self.canvas.draw()

        print(f"Multiple data plot created with selected datasets: {selected_labels}, Marker: {marker}, Color: {color}")
        self.accept()

