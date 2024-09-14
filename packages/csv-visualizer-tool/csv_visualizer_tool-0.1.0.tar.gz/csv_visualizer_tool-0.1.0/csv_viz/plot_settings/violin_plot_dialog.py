from PyQt5.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QFormLayout, QComboBox, QCheckBox, QDialogButtonBox
from ..visualizations import plot_violin
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QWidget


class ViolinPlotDialog(QDialog):
    def __init__(self, df, canvas):
        super().__init__()
        self.df = df
        self.canvas = canvas
        self.setWindowTitle('Violin Plot Settings')

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
        button_box.accepted.connect(self.plot_violin)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def _create_general_tab(self):
        """Create the general tab for violin plot settings."""
        general_tab = QWidget()
        general_layout = QFormLayout()

        self.column_combo = QComboBox(self)
        self.column_combo.addItems(self.df.columns)
        general_layout.addRow("Select Column(s):", self.column_combo)

        self.orientation_combo = QComboBox(self)
        self.orientation_combo.addItems(["Vertical", "Horizontal"])
        general_layout.addRow("Orientation:", self.orientation_combo)

        general_tab.setLayout(general_layout)
        return general_tab

    def _create_aesthetics_tab(self):
        """Create the aesthetics tab for violin plot settings."""
        aesthetics_tab = QWidget()
        aesthetics_layout = QFormLayout()

        self.split_checkbox = QCheckBox("Split Violin (For binary categorical data)")
        aesthetics_layout.addRow(self.split_checkbox)

        aesthetics_tab.setLayout(aesthetics_layout)
        return aesthetics_tab

    def plot_violin(self):
        """Plot the violin plot using the selected options."""
        column = self.column_combo.currentText()
        orientation = self.orientation_combo.currentText().lower()
        split = self.split_checkbox.isChecked()

        # Clear previous plot
        self.canvas.figure.clear()

        # Call the plot function from visualizations
        plot_violin(self.canvas.figure, self.df[[column]], orientation=orientation, split=split)
        self.canvas.draw()

        print(f"Violin plot created for column: {column}, Orientation: {orientation}, Split: {split}")
        self.accept()

