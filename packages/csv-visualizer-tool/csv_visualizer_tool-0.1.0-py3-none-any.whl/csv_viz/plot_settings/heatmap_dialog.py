from PyQt5.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QFormLayout, QComboBox, QCheckBox, QDialogButtonBox
from ..visualizations import plot_heatmap
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QWidget


class HeatmapDialog(QDialog):
    def __init__(self, df, canvas):
        super().__init__()
        self.df = df
        self.canvas = canvas
        self.setWindowTitle('Heatmap Settings')

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
        button_box.accepted.connect(self.plot_heatmap)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def _create_general_tab(self):
        """Create the general tab for heatmap settings."""
        general_tab = QWidget()
        general_layout = QFormLayout()

        self.x_combo = QComboBox(self)
        self.x_combo.addItems(self.df.columns)
        general_layout.addRow("Select X Axis:", self.x_combo)

        self.y_combo = QComboBox(self)
        self.y_combo.addItems(self.df.columns)
        general_layout.addRow("Select Y Axis:", self.y_combo)

        general_tab.setLayout(general_layout)
        return general_tab

    def _create_aesthetics_tab(self):
        """Create the aesthetics tab for heatmap settings."""
        aesthetics_tab = QWidget()
        aesthetics_layout = QFormLayout()

        self.colormap_combo = QComboBox(self)
        self.colormap_combo.addItems(["viridis", "coolwarm", "plasma", "inferno"])
        aesthetics_layout.addRow("Colormap:", self.colormap_combo)

        self.annotate_checkbox = QCheckBox("Annotate cells")
        aesthetics_layout.addRow(self.annotate_checkbox)

        aesthetics_tab.setLayout(aesthetics_layout)
        return aesthetics_tab

    def plot_heatmap(self):
        """Plot the heatmap using the selected options."""
        x_column = self.x_combo.currentText()
        y_column = self.y_combo.currentText()
        colormap = self.colormap_combo.currentText()
        annotate = self.annotate_checkbox.isChecked()

        # Clear previous plot
        self.canvas.figure.clear()

        # Call the plot function from visualizations
        plot_heatmap(self.canvas.figure, self.df[[x_column, y_column]], colormap=colormap, annotate=annotate)
        self.canvas.draw()

        print(f"Heatmap created with X: {x_column}, Y: {y_column}, Colormap: {colormap}, Annotate: {annotate}")
        self.accept()

