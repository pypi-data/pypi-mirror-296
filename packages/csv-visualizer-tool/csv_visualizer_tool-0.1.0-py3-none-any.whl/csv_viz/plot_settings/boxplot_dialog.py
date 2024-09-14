from PyQt5.QtWidgets import QDialog, QTabWidget, QVBoxLayout, QFormLayout, QComboBox, QCheckBox, QDialogButtonBox
from ..visualizations import plot_boxplot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QColorDialog

class BoxPlotDialog(QDialog):
    def __init__(self, df, canvas):
        super().__init__()
        self.df = df
        self.canvas = canvas
        self.setWindowTitle('Boxplot Settings')

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
        button_box.accepted.connect(self.plot_boxplot)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def _create_general_tab(self):
        """Create the general tab for boxplot settings."""
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
        """Create the aesthetics tab for boxplot settings."""
        aesthetics_tab = QWidget()
        aesthetics_layout = QFormLayout()

        self.box_width_combo = QComboBox(self)
        self.box_width_combo.addItems(["0.5", "0.8", "1.0"])
        aesthetics_layout.addRow("Box Width:", self.box_width_combo)

        self.showfliers_checkbox = QCheckBox("Show Fliers")
        aesthetics_layout.addRow(self.showfliers_checkbox)

        aesthetics_tab.setLayout(aesthetics_layout)
        return aesthetics_tab

    def plot_boxplot(self):
        """Plot the boxplot using the selected options."""
        column = self.column_combo.currentText()
        orientation = self.orientation_combo.currentText().lower()
        box_width = float(self.box_width_combo.currentText())
        show_fliers = self.showfliers_checkbox.isChecked()

        # Clear previous plot
        self.canvas.figure.clear()

        # Call the plot function from visualizations
        plot_boxplot(self.canvas.figure, self.df[[column]], orientation=orientation, box_width=box_width, show_fliers=show_fliers)
        self.canvas.draw()

        print(f"Boxplot created for column: {column}, Orientation: {orientation}, Box Width: {box_width}, Show Fliers: {show_fliers}")
        self.accept()

