from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QCheckBox, QDialogButtonBox
from ..visualizations import plot_pairplot
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QWidget


class PairPlotDialog(QDialog):
    def __init__(self, df, canvas):
        super().__init__()
        self.df = df
        self.canvas = canvas
        self.setWindowTitle('Pairplot Settings')

        # Create layout
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Selecting columns and features
        self.hue_combo = QComboBox(self)
        self.hue_combo.addItems(["None"] + list(self.df.columns))  # "None" option for no hue
        form_layout.addRow("Hue (optional):", self.hue_combo)

        self.kind_combo = QComboBox(self)
        self.kind_combo.addItems(['scatter', 'reg', 'kde'])
        form_layout.addRow("Kind:", self.kind_combo)

        self.diag_kind_combo = QComboBox(self)
        self.diag_kind_combo.addItems(['auto', 'kde', 'hist'])
        form_layout.addRow("Diagonal Type:", self.diag_kind_combo)

        self.palette_combo = QComboBox(self)
        self.palette_combo.addItems(['deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind'])
        form_layout.addRow("Color Palette:", self.palette_combo)

        self.corner_checkbox = QCheckBox('Corner (Only lower triangle)')
        form_layout.addRow(self.corner_checkbox)

        layout.addLayout(form_layout)

        # Buttons for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.plot_pairplot)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def plot_pairplot(self):
        """Plot the pairplot based on user settings."""
        hue = self.hue_combo.currentText()
        kind = self.kind_combo.currentText()
        diag_kind = self.diag_kind_combo.currentText()
        palette = self.palette_combo.currentText()
        corner = self.corner_checkbox.isChecked()

        # Adjusting the hue in case "None" is selected
        hue = None if hue == "None" else hue

        # Clear previous plot
        self.canvas.figure.clear()

        # Call the plot function from visualizations
        plot_pairplot(self.canvas.figure, self.df, hue=hue, kind=kind, diag_kind=diag_kind, palette=palette, corner=corner)
        self.canvas.draw()

        print(f"Pairplot created with Hue: {hue}, Kind: {kind}, Diagonal: {diag_kind}, Palette: {palette}, Corner: {corner}")
        self.accept()

