from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QInputDialog, QMessageBox

class DataOperationsDialog(QDialog):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.filtered_df = df.copy()
        self.setWindowTitle("Data Operations")

        layout = QVBoxLayout()

        sort_button = QPushButton('Sort Data')
        sort_button.clicked.connect(self.sort_data)
        layout.addWidget(sort_button)

        filter_button = QPushButton('Filter Data')
        filter_button.clicked.connect(self.filter_data)
        layout.addWidget(filter_button)

        groupby_button = QPushButton('Group By')
        groupby_button.clicked.connect(self.groupby_data)
        layout.addWidget(groupby_button)

        self.setLayout(layout)

    def sort_data(self):
        """Sort data by a selected column."""
        if self.df.empty:
            QMessageBox.warning(self, "Error", "Dataframe is empty.")
            return

        column, ok = QInputDialog.getItem(self, "Select Column", "Sort by column:", self.df.columns, 0, False)
        if ok and column:
            self.filtered_df = self.df.sort_values(by=[column])
            print(f"Data sorted by column: {column}")

    def filter_data(self):
        """Filter data by a selected column and value."""
        if self.df.empty:
            QMessageBox.warning(self, "Error", "Dataframe is empty.")
            return

        column, ok = QInputDialog.getItem(self, "Select Column", "Filter by column:", self.df.columns, 0, False)
        if ok and column:
            value, ok = QInputDialog.getText(self, "Filter", f"Enter value for {column}:")
            if ok and value:
                self.filtered_df = self.df[self.df[column] == value]
                print(f"Data filtered by {column} = {value}")

    def groupby_data(self):
        """Group data by a selected column."""
        if self.df.empty:
            QMessageBox.warning(self, "Error", "Dataframe is empty.")
            return

        column, ok = QInputDialog.getItem(self, "Select Column", "Group by column:", self.df.columns, 0, False)
        if ok and column:
            grouped_df = self.df.groupby(column).mean()  # Group by the selected column and calculate the mean
            self.filtered_df = grouped_df
            print(f"Data grouped by column: {column}")

