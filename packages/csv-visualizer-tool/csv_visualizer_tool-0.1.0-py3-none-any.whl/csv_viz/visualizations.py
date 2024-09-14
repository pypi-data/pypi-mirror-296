import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

def plot_scatter(
    fig, df, marker='o', marker_size=10, color=None, log_scale=False,
    add_trendline=False, error_bars=False, gridlines=False
):
    """Plot a scatter plot with optional trendline, error bars, and gridlines."""
    if df.shape[1] < 2:
        raise ValueError("DataFrame must have at least two columns for a scatter plot.")
    
    fig.clear()  # Ensure the previous plot is cleared
    ax = fig.add_subplot(111)
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]

    if log_scale:
        if (x <= 0).any() or (y <= 0).any():
            raise ValueError("Log scale cannot be applied to non-positive values.")
        ax.set_xscale('log')
        ax.set_yscale('log')

    ax.scatter(x, y, marker=marker, s=marker_size, color=color)

    if add_trendline:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        ax.plot(x, slope * x + intercept, 'r', label=f'Trend: y={slope:.2f}x + {intercept:.2f}')
        ax.legend()

    if error_bars:
        y_err = df.iloc[:, 1].std()
        ax.errorbar(x, y, yerr=y_err, fmt='none', ecolor='gray', alpha=0.5)

    if gridlines:
        ax.grid(True)

    ax.set_title('Scatter Plot')
    ax.set_xlabel(df.columns[0])
    ax.set_ylabel(df.columns[1])


def plot_boxplot(fig, df, orientation='vertical', box_width=0.8, show_fliers=True):
    """Plot a boxplot with options for orientation, box width, and showing fliers."""
    fig.clear()  # Ensure the previous plot is cleared
    ax = fig.add_subplot(111)

    sns.boxplot(data=df, orient=orientation, width=box_width, showfliers=show_fliers, ax=ax)
    
    ax.set_title('Box Plot')
    ax.set_ylabel('Values' if orientation == 'vertical' else 'Columns')
    ax.set_xlabel('Columns' if orientation == 'vertical' else 'Values')


def plot_heatmap(fig, df, colormap='viridis', annotate=False):
    """Plot a heatmap with options for colormap and annotation."""
    fig.clear()  # Ensure the previous plot is cleared
    ax = fig.add_subplot(111)

    # Compute correlation matrix if df has multiple columns
    if df.shape[1] > 1:
        df = df.corr()

    sns.heatmap(df, cmap=colormap, annot=annotate, ax=ax)

    ax.set_title('Heatmap')


def plot_violin(fig, df, orientation='vertical', split=False):
    """Plot a violin plot with options for orientation and splitting."""
    fig.clear()  # Ensure the previous plot is cleared
    ax = fig.add_subplot(111)

    sns.violinplot(data=df, orient=orientation, split=split, ax=ax)
    
    ax.set_title('Violin Plot')
    ax.set_ylabel('Values' if orientation == 'vertical' else 'Columns')
    ax.set_xlabel('Columns' if orientation == 'vertical' else 'Values')


def plot_trendline(fig, df, marker='o', color=None, log_scale=False):
    """Plot a trendline with the given options."""
    if df.shape[1] < 2:
        raise ValueError("DataFrame must have at least two columns for a trendline.")
    
    fig.clear()  # Ensure the previous plot is cleared
    ax = fig.add_subplot(111)

    # Convert the Pandas Series to NumPy arrays
    x = df.iloc[:, 0].to_numpy()
    y = df.iloc[:, 1].to_numpy()

    if log_scale:
        if (x <= 0).any() or (y <= 0).any():
            raise ValueError("Log scale cannot be applied to non-positive values.")
        ax.set_xscale('log')
        ax.set_yscale('log')

    # Perform linear regression using NumPy arrays
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    ax.plot(x, slope * x + intercept, 'r', label=f'Trend: y={slope:.2f}x + {intercept:.2f}')
    ax.scatter(x, y, marker=marker, color=color)
    ax.legend()

    ax.set_title('Trend Line Plot')
    ax.set_xlabel(df.columns[0])
    ax.set_ylabel(df.columns[1])


def plot_with_error_bars(fig, df, marker='o', color=None, log_scale=False):
    """Plot data with error bars."""
    if df.shape[1] < 2:
        raise ValueError("DataFrame must have at least two columns for plotting error bars.")
    
    fig.clear()  # Ensure the previous plot is cleared
    ax = fig.add_subplot(111)
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]

    if log_scale:
        if (x <= 0).any() or (y <= 0).any():
            raise ValueError("Log scale cannot be applied to non-positive values.")
        ax.set_xscale('log')
        ax.set_yscale('log')

    y_err = df.iloc[:, 1].std()
    ax.errorbar(x, y, yerr=y_err, fmt=marker, ecolor='gray', color=color)

    ax.set_title('Plot with Error Bars')
    ax.set_xlabel(df.columns[0])
    ax.set_ylabel(df.columns[1])


def plot_multiple(fig, df_list, labels, marker='o', color=None, log_scale=False):
    """Plot multiple data sets on the same figure."""
    fig.clear()  # Ensure the previous plot is cleared
    ax = fig.add_subplot(111)

    for i, df in enumerate(df_list):
        if df.shape[1] < 2:
            raise ValueError("Each DataFrame in df_list must have at least two columns.")
        
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]

        if log_scale:
            if (x <= 0).any() or (y <= 0).any():
                raise ValueError(f"Log scale cannot be applied to non-positive values in DataFrame {i+1}.")
            ax.set_xscale('log')
            ax.set_yscale('log')

        ax.scatter(x, y, marker=marker, color=color, label=labels[i])

    ax.legend()
    ax.set_title('Multiple Data Plot')
    ax.set_xlabel(df_list[0].columns[0])
    ax.set_ylabel(df_list[0].columns[1])


def plot_histogram(fig, df, bins=10, color='blue', log_scale=False):
    """Plot a histogram with the option for a logarithmic scale."""
    if df.shape[1] < 1:
        raise ValueError("DataFrame must have at least one column for a histogram.")
    
    fig.clear()  # Ensure the previous plot is cleared
    ax = fig.add_subplot(111)
    data = df.iloc[:, 0]

    if log_scale:
        if (data <= 0).any():
            raise ValueError("Log scale cannot be applied to non-positive values in the histogram.")
        ax.set_xscale('log')

    ax.hist(data, bins=bins, color=color)

    ax.set_title('Histogram')
    ax.set_xlabel(df.columns[0])
    ax.set_ylabel('Frequency')


def plot_pairplot(fig, df, hue=None, kind='scatter', diag_kind='auto', palette='deep', corner=False):
    """Plot a pairplot with options for hue, kind, diagonal type, palette, and corner."""
    sns.pairplot(df, hue=hue, kind=kind, diag_kind=diag_kind, palette=palette, corner=corner)
    # No need to use fig.clear() or fig.suptitle() since Seaborn handles figure management


def plot_catplot(fig, df, x, y, hue=None, kind='strip', col_wrap=None, dodge=False):
    """Plot a categorical plot (catplot) with options for hue, kind, col_wrap, and dodge."""
    sns.catplot(data=df, x=x, y=y, hue=hue, kind=kind, col_wrap=col_wrap, dodge=dodge)
    # No need to use fig.clear() or fig.suptitle() since Seaborn handles figure management

