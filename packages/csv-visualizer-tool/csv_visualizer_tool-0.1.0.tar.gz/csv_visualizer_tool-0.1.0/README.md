# CSV Visualization Tool

This project provides a graphical user interface (GUI) for visualizing CSV data using various Seaborn and Matplotlib plots. The GUI is built using PyQt5 and supports multiple types of plots including scatter plots, box plots, violin plots, and more. It also allows for features like trendlines, error bars, and logarithmic scaling.

## Features

- **Scatter Plot** with optional trendline, gridlines, and error bars.
- **Box Plot** with options for orientation and flier visibility.
- **Violin Plot** with customizable orientation and splitting.
- **Heatmap** to visualize correlation matrices or any numerical data.
- **Pair Plot** and **Categorical Plot (Catplot)**.
- **Histogram** with optional logarithmic scale.
- **Multiple Data Plotting** for visualizing multiple datasets on the same axes.
- **Logarithmic scaling** on x and y axes.
- **Interactive GUI** to easily select CSV files and configure plots.

---

### Requirements

This project depends on the following Python libraries:

- `pandas >= 1.3.0`
- `matplotlib >= 3.4.0`
- `seaborn >= 0.11.2`
- `PyQt5 >= 5.12`
  
You can install these dependencies via `pip`:

```bash
pip install -r requirements.txt
```

Or using `conda`:

```bash
conda install pandas matplotlib seaborn pyqt
```

---

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/chandrasekarnarayana/csv_viz.git
   cd csv_viz
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   After installing the dependencies, you can run the application using the following command:

   ```bash
   csv_viz
   ```

   Alternatively, you can run it directly via Python:

   ```bash
   python -m csv_viz.main_window
   ```

---

### Usage

1. **Launching the Application**: Upon running the application, a GUI window will open. Use the "Load CSV" button to load your CSV file. After loading, you can choose the type of plot you want to generate using the dropdown list.

2. **Viewing CSV Data**: You can view the raw CSV data by clicking on the "View CSV Data" button.

3. **Statistics**: View statistics such as mean, median, and standard deviation of the data by clicking on the "View Statistics" button.

4. **Creating Plots**: Use the "Plot Data" button to configure and create plots. You can specify various parameters such as the type of plot, marker style, gridlines, trendlines, and logarithmic scaling.

5. **Data Operations**: Filter, sort, and group your data using the "Data Operations" button.

---

### Example

Here is an example workflow to visualize data:

1. Run the application with the command:

   ```bash
   csv_viz
   ```

2. Load your CSV file by clicking the "Load CSV" button.

3. Select the type of plot (e.g., "Scatter Plot") and click "Plot Data."

4. Adjust the plot settings in the dialog window (e.g., marker size, trendlines, etc.).

5. View your generated plot in the main window.

---

### Troubleshooting

1. **ModuleNotFoundError**: If you encounter this error for any package, ensure all dependencies are installed correctly:

   ```bash
   pip install -r requirements.txt
   ```

2. **Logarithmic Scale Errors**: If your data contains zeros or negative values, the logarithmic scale option will not work. Ensure all values are positive when using log scaling.

---

### Contributing

Feel free to contribute to this project by submitting issues or pull requests. Please ensure all contributions follow PEP8 guidelines and include appropriate documentation.

---

### License

This project is licensed under the GPLv3.0.

---

### Author

Chandrasekar Subramani Narayana  
[Email](mailto:chandrasekarnarayana@gmail.com)

---

### Version

#### 0.1.0
