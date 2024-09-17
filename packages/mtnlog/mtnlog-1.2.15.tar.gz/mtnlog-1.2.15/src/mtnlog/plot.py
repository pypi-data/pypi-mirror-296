"""
PerformancePlotter Module
=========================
This module provides the `PerformancePlotter` class for plotting performance metrics from CSV files. 
It visualizes various system metrics such as CPU usage, memory usage, network bandwidth, and GPU utilization.

The plots are saved as images in a specified directory, providing an easy way to analyze the system's performance 
over time.

Classes:
--------
- PerformancePlotter: A class for reading performance metrics from CSV files and plotting them into graphs.

Dependencies:
-------------
- `logging`: For logging information, warnings, and errors.
- `os`: For file and directory management.
- `re`: For regular expressions to clean up plot labels.
- `typing`: For type annotations.
- `matplotlib`: For plotting the performance metrics.
- `pandas`: For handling the performance data in DataFrame format.
- `tqdm`: For showing a progress bar during the plotting process.
"""

import logging
import os
import re
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
from pandas.errors import EmptyDataError, ParserError
from tqdm import tqdm

cuda_devices: List[int] = [0, 1, 2, 3]

network_interfaces: List[str] = ['lo', 'enp195s0', 'bond0', 'hsn0', 'hsn1']

plot_col: List[str] = [
    'cpu_percent (%)/mean',
    'memory_used (GiB)/mean',
    'memory_percent (%)/mean'
] + [
    f'cuda:{i} (gpu:{i})/{metric}/mean'
    for i in cuda_devices
    for metric in ['memory_used (MiB)', 'gpu_utilization (%)']
] + [
    f'network_{interface}/{direction} (Mbps)'
    for interface in network_interfaces
    for direction in ['sent', 'recv']
]

tag_colors_map: Dict[str, str] = {
    'load_model': 'blue',
    'load_token': 'green',
    'load_data': 'orange',
    'load_trainer': 'purple',
    'train': 'red',
    'save_model': 'brown'
}

line_styles: List[str] = ['-', '--', '-.', ':']

fallback_colors = plt.get_cmap("Set1").colors

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PerformancePlotter:
    """
    PerformancePlotter
    ==================
    A class to plot performance metrics for a specified node from a CSV file. The class can generate 
    various types of plots including CPU usage, memory usage, network bandwidth, and GPU utilization.

    Attributes:
    -----------
    - log_node (str): Identifier for the node whose metrics are to be plotted.
    - metric_dir (str): Directory where the metrics CSV files are located.
    - graph_dir (str): Directory where the generated plots will be saved.

    Methods:
    --------
    - get_tag_colors(df: pd.DataFrame) -> Dict[str, str]: Returns a color mapping for each tag in the DataFrame.
    - graph(df: pd.DataFrame, node_plot_dir: str) -> None: Plots the metrics for the given node and saves the plots.
    - plot_cuda_memory(df: pd.DataFrame, node_plot_dir: str) -> None: Plots CUDA memory usage for all GPUs.
    - plot() -> None: Reads the metrics from a CSV file and generates plots for the given node.
    """

    def __init__(self, base_dir: str, log_node: str):
        """
        Initializes the PerformancePlotter with the base directory and node identifier.

        Parameters:
        -----------
        - base_dir (str): The base directory containing the metrics and where the plots will be saved.
        - log_node (str): Identifier for the node whose metrics are to be plotted.
        """
        self.log_node: str = log_node
        self.metric_dir: str = f"{base_dir}/metric"
        self.graph_dir: str = f"{base_dir}/graph"
        os.makedirs(self.graph_dir, exist_ok=True)

    def get_tag_colors(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Get colors for each tag in the DataFrame to differentiate them in the plots.

        Parameters:
        -----------
        - df (pd.DataFrame): The DataFrame containing performance metrics.

        Returns:
        --------
        - Dict[str, str]: A dictionary mapping each unique tag in the DataFrame to a color.
        """
        tags = df['tag'].unique()
        return {
            tag: tag_colors_map.get(tag, fallback_colors[i % len(fallback_colors)])
            for i, tag in enumerate(tags)
        }

    def graph(self, df: pd.DataFrame, node_plot_dir: str) -> None:
        """
        Plot metrics for the given node and save them as images.

        This method generates line plots for each performance metric in the DataFrame. It differentiates 
        segments of data based on tags and applies specific styles and colors to each segment.

        Parameters:
        -----------
        - df (pd.DataFrame): The DataFrame containing performance metrics.
        - node_plot_dir (str): Directory where the plots for this node will be saved.
        """
        os.makedirs(node_plot_dir, exist_ok=True)
        tag_colors = self.get_tag_colors(df)

        for col in tqdm(plot_col, desc=f"Plotting metrics for node-{self.log_node}: "):
            if col not in df.columns:
                logging.warning("Column %s not found in DataFrame, skipping.", col)
                continue

            _, ax = plt.subplots(figsize=(10, 6))
            segment = None  # Define segment outside the loop to avoid undefined variable

            for tag, segment in df.groupby('tag'):
                segment['duration (s)'] = pd.to_numeric(segment['duration (s)'], errors='coerce')
                segment[col] = pd.to_numeric(segment[col], errors='coerce')
                segment = segment.dropna(subset=['duration (s)', col])

                if not segment.empty:
                    ax.plot(segment['duration (s)'], segment[col], label=tag, color=tag_colors[tag])

            if segment is not None and not segment.empty:
                # Add max memory line for GPU memory usage metrics
                if 'memory_used (MiB)' in col:
                    gpu_memory_col = col.replace('memory_used (MiB)', 'memory_total (MiB)')
                    if gpu_memory_col in df.columns:
                        df[gpu_memory_col] = pd.to_numeric(df[gpu_memory_col], errors='coerce')
                        max_y = df[gpu_memory_col].mean()
                        if not pd.isna(max_y):
                            ax.axhline(y=max_y, color='red', linestyle='-', label="Max Memory")

                # Add max RAM usage line for memory_used (GiB)
                if 'memory_used (GiB)' and 'total_ram (GB)' in col:
                    # Calculate max RAM usage
                    max_ram = df['total_ram (GiB)'].max()
                    if not pd.isna(max_ram):
                        ax.axhline(y=max_ram, color='red', linestyle='-', label="Max RAM")
                        # Set y-axis limit to start from 0 up to max_ram
                        ax.set_ylim(0, max_ram)

                # Set y-axis limit to 100% for percentage metrics
                if '%' in col:
                    ax.set_ylim(0, 100)

                ax.legend(title='Tag')
                name = re.sub(r"[ /]", "_", col)
                name = re.sub(r"_mean", "", name)
                name = re.sub(r"\(gpu:\d+\)", "", name)

                ax.set_xlabel('Duration (s)')
                ax.set_ylabel(name)

                if 'cuda:' in col:
                    gpu_num = re.search(r'cuda:(\d+)', col).group(1)
                    last_point = segment['duration (s)'].iloc[-1]
                    last_value = segment[col].iloc[-1]
                    ax.text(last_point, last_value, f'GPU {gpu_num}', fontsize=9,
                            color=tag_colors[df['tag'].iloc[-1]],
                            ha='left', va='bottom', rotation=45)

                plt.tight_layout()
                plt.savefig(f"{node_plot_dir}/{name}.jpg", format='jpeg', dpi=100, bbox_inches='tight')
                plt.close()

    def plot_cuda_memory(self, df: pd.DataFrame, node_plot_dir: str) -> None:
        """
        Plot CUDA memory usage for all GPUs and save the plot.

        This method generates a combined plot showing memory usage for all available CUDA devices. It also includes 
        a line indicating the maximum memory for each device.

        Parameters:
        -----------
        - df (pd.DataFrame): The DataFrame containing CUDA memory usage metrics.
        - node_plot_dir (str): Directory where the CUDA memory plot will be saved.
        """
        _, ax = plt.subplots(figsize=(14, 8))
        tag_colors = self.get_tag_colors(df)

        for i, cuda_device in enumerate(cuda_devices):
            col = f'cuda:{cuda_device} (gpu:{cuda_device})/memory_used (MiB)/mean'
            max_col = f'cuda:{cuda_device} (gpu:{cuda_device})/memory_total (MiB)/mean'

            if col in df.columns:
                for tag in df['tag'].unique():
                    segment = df[df['tag'] == tag]
                    if segment.empty:
                        continue
                    ax.plot(segment['duration (s)'], segment[col], label=tag if i == 0 else "",
                            color=tag_colors[tag], linestyle=line_styles[i])

                    last_point = segment['duration (s)'].iloc[-1]
                    last_value = segment[col].iloc[-1]
                    ax.text(last_point, last_value, f'GPU {cuda_device}', fontsize=9, color=tag_colors[tag],
                            ha='left', va='bottom', rotation=45)

                if max_col in df.columns:
                    max_memory = df[max_col].max()
                    ax.axhline(y=max_memory, color=tag_colors[list(tag_colors.keys())[i % len(tag_colors)]],
                               linestyle=':', label=f'Max GPU {cuda_device}')
                    ax.text(df['duration (s)'].max(), max_memory, f'Max GPU {cuda_device}: {max_memory:.0f} MiB',
                            fontsize=9, color=tag_colors[list(tag_colors.keys())[i % len(tag_colors)]],
                            ha='right', va='bottom')

        ax.set_xlabel('Duration (s)')
        ax.set_ylabel('Memory Used (MiB)')
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = dict(zip(labels, handles))
        ax.legend(unique_labels.values(), unique_labels.keys(), title='Tag', loc='upper left', bbox_to_anchor=(1, 1))

        plt.tight_layout()
        plt.savefig(f"{node_plot_dir}/cuda_memory_used_all.jpg", format='jpeg', dpi=100, bbox_inches='tight')
        plt.close()

    def plot(self) -> None:
        """
        Plot metrics for the given node by reading the CSV file and generating the plots.

        This method reads the performance metrics from a CSV file for the specified node, processes the data, 
        and generates various plots including individual metric plots and CUDA memory usage plots.

        Raises:
        -------
        - EmptyDataError: If the CSV file is empty.
        - ParserError: If the CSV file is improperly formatted.
        - OSError: If there is an error reading the file.
        """
        filepath = f"{self.metric_dir}/node-{self.log_node}.csv"

        try:
            # Read CSV with low_memory=False to avoid chunking and DtypeWarning
            df = pd.read_csv(filepath, low_memory=False)

            if df.empty:
                logging.warning("File %s is empty, skipping.", filepath)
                return

            # Convert 'duration (s)' to numeric, forcing non-numeric to NaN
            df['duration (s)'] = pd.to_numeric(df['duration (s)'], errors='coerce')

            # Add this line to drop rows with NaN in 'duration (s)'
            df = df.dropna(subset=['duration (s)'])

            # Sort the dataframe by 'duration (s)'
            df.sort_values(by=['duration (s)'], inplace=True)

            # Filter out rows where the 'tag' column is NaN
            df = df[df['tag'].notna()]
            node_plot_dir = f"{self.graph_dir}/node-{self.log_node}"

            # Ensure all relevant columns are cast to numeric where applicable
            for col in df.columns:
                if col in plot_col:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Continue with plotting
            self.graph(df, node_plot_dir)
            self.plot_cuda_memory(df, node_plot_dir)

        except EmptyDataError:
            logging.warning("File %s is empty, skipping.", filepath)
        except ParserError:
            logging.error("File %s is improperly formatted, skipping.", filepath)
        except OSError as e:
            logging.error("Error reading file %s: %s", filepath, e)

        logging.info("Graphs saved in %s", self.graph_dir)
