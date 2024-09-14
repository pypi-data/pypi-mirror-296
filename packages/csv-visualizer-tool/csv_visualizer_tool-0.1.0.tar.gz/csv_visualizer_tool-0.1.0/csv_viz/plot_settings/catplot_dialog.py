from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QCheckBox, QDialogButtonBox
from ..visualizations import plot_catplot
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QWidget


class CatPlotDialog(QDialog):
    def __init__(self, df, canvas):
        super().__init__()
        self.df = df
        self.canvas = canvas
        self.setWindowTitle('Catplot Settings')

        # Create layout
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Selecting columns and features
        self.x_combo = QComboBox(self)
        self.x_combo.addItems(self.df.columns)
        form_layout.addRow("Select X column:", self.x_combo)

        self.y_combo = QComboBox(self)
        self.y_combo.addItems(self.df.columns)
        form_layout.addRow("Select Y column:", self.y_combo)

        self.hue_combo = QComboBox(self)
        self.hue_combo.addItems(["None"] + list(self.df.columns))  # "None" option for no hue
        form_layout.addRow("Hue (optional):", self.hue_combo)

        self.kind_combo = QComboBox(self)
        self.kind_combo.addItems(['strip', 'swarm', 'box', 'violin', 'bar', 'count', 'point'])
        form_layout.addRow("Kind:", self.kind_combo)

        self.col_wrap_spinbox = QComboBox(self)
        self.col_wrap_spinbox.addItems(["1", "2", "3", "4"])
        form_layout.addRow("Col Wrap:", self.col_wrap_spinbox)

        self.dodge_checkbox = QCheckBox('Dodge (grouped plots)')
        form_layout.addRow(self.dodge_checkbox)

        layout.addLayout(form_layout)

        # Buttons for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.plot_catplot)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def plot_catplot(self):
        """Plot the catplot based on user settings."""
        x_column = self.x_combo.currentText()
        y_column = self.y_combo.currentText()
        hue = self.hue_combo.currentText()
        kind = self.kind_combo.currentText()
        col_wrap = int(self.col_wrap_spinbox.currentText())
        dodge = self.dodge_checkbox.isChecked()

        # Adjusting the hue in case "None" is selected
        hue = None if hue == "None" else hue

        # Clear previous plot
        self.canvas.figure.clear()

        # Call the plot function from visualizations
        plot_catplot(self.canvas.figure, self.df, x=x_column, y=y_column, hue=hue, kind=kind, col_wrap=col_wrap, dodge=dodge)
        self.canvas.draw()

        print(f"Catplot created with X: {x_column}, Y: {y_column}, Hue: {hue}, Kind: {kind}, Col Wrap: {col_wrap}, Dodge: {dodge}")
        self.accept()

