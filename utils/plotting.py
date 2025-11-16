"""
Plotting utilities and styling
Shared matplotlib/seaborn configuration
"""
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Set backend for tkinter integration
matplotlib.use('TkAgg')

def setup_plot_style():
    """
    Configure consistent plot style across application
    Called once at app startup
    """
    sns.set_style("whitegrid")
    plt.rcParams['font.size'] = 9
    plt.rcParams['figure.figsize'] = (8, 6)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['axes.labelsize'] = 9
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['legend.fontsize'] = 8

def create_figure(figsize=(8, 6), dpi=100):
    """
    Create new matplotlib figure with standard settings

    Args:
        figsize: Figure size (width, height) in inches
        dpi: Dots per inch

    Returns:
        fig, ax: Figure and axes objects
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.grid(True, alpha=0.3)
    return fig, ax

def format_axis_labels(ax, xlabel='', ylabel='', title=''):
    """
    Format axis labels and title

    Args:
        ax: Matplotlib axes object
        xlabel: X-axis label
        ylabel: Y-axis label
        title: Plot title
    """
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
