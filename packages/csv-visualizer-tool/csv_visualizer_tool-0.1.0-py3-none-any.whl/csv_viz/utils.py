import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def load_csv(file_path):
    """Load a CSV file and return a pandas DataFrame"""
    try:
        df = pd.read_csv(file_path)
        print(f"CSV file loaded successfully from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

def save_plot(figure, file_path):
    """Save the current plot to a file"""
    figure.savefig(file_path)
    print(f"Plot saved to {file_path}")

def export_filtered_data(df, file_path):
    """Export the filtered DataFrame to a CSV file"""
    df.to_csv(file_path, index=False)
    print(f"Filtered data exported to {file_path}")

