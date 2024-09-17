"""
PerformanceLogger Module
========================
This module provides a `PerformanceLogger` class for logging system performance metrics such as CPU usage, 
network bandwidth, and GPU utilization using multiprocessing. It collects and writes metrics to a CSV file at 
specified intervals.

Classes:
--------
- PerformanceLogger: A class for logging performance metrics, supporting custom tagging and interval-based data collection.

Dependencies:
-------------
- `psutil`: For system and network metrics collection.
- `nvitop`: For GPU resource metric collection.
- `pandas`: For handling metrics data in DataFrame format.
- `csv`: For writing metrics data to a CSV file.
- `logging`: For logging information, warnings, and errors.
- `os`: For file and directory management.
- `time`: For interval management.
- `multiprocessing`: For running the collector and writer processes concurrently.
"""

import csv
import logging
import os
import time
from multiprocessing import Process, Queue, Event
from queue import Empty
from typing import Union, Dict, Optional, cast

import pandas as pd
import psutil
from nvitop import Device, ResourceMetricCollector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PerformanceLogger:
    """
    PerformanceLogger
    =================
    A class to log performance metrics such as CPU usage per core, network bandwidth, and GPU metrics. 
    Utilizes multiprocessing to collect and write metrics concurrently to a CSV file.

    Attributes:
    -----------
    - filepath (str): The file path for saving the metrics log.
    - log_dir (str): The directory where logs are stored.
    - log_node (str): A unique identifier for the logging node.
    - debug_mode (bool): If True, enables detailed logging for debugging purposes.
    - interval (float): The interval in seconds at which metrics are collected.
    - cpu_count (int): The number of physical CPU cores.
    - stop_event (Event): An event to signal the stopping of metric collection.
    - metrics_queue (Queue): A queue for holding collected metrics.
    - tag_queue (Queue): A queue for managing custom tags for the metrics.

    Methods:
    --------
    - stop(): Stops the collector and writer processes and closes the queues.
    - change_tag(tag: str): Changes the tag associated with the collected metrics.
    """

    def __init__(self, log_dir: str, log_node: str, interval: float = 1.0, debug_mode: bool = False):
        """
        Initializes the PerformanceLogger with the specified logging directory, node identifier, interval, 
        and debug mode.

        Parameters:
        -----------
        - log_dir (str): Directory where the log file will be stored.
        - log_node (str): Identifier for the logging node, included in the log file name.
        - interval (float): Interval in seconds between each metrics collection (default is 1.0).
        - debug_mode (bool): Enables detailed logging if set to True (default is False).
        """
        os.makedirs(log_dir, exist_ok=True)

        self.filepath = f"{log_dir}/node-{log_node}.csv"
        self.log_dir = log_dir
        self.log_node = log_node
        self.debug_mode = debug_mode
        self.interval = interval
        self.cpu_count = psutil.cpu_count(logical=False)
        self.stop_event = Event()
        self.metrics_queue = Queue()
        self.tag_queue = Queue()  # Queue for managing custom tags

        # Start custom processes for collecting and writing metrics
        self.collector_process = Process(target=self._run_collector, args=(
            self.stop_event, self.metrics_queue, self.tag_queue, self.interval))
        self.writer_process = Process(target=self._run_writer,
                                      args=(self.stop_event, self.metrics_queue, self.filepath))
        self.collector_process.start()
        self.writer_process.start()

    def stop(self) -> None:
        """
        Stops the performance logger processes. This method sets the stop event to terminate the
        collector and writer processes, and ensures all queues are properly closed.
        """
        self.stop_event.set()
        self.collector_process.join()
        self.writer_process.join()
        self.metrics_queue.close()
        self.tag_queue.close()

    def change_tag(self, tag: str) -> None:
        """
        Changes the tag associated with the metrics being collected. This tag is included in the log output
        to help differentiate between different stages or types of metrics collection.

        Parameters:
        -----------
        - tag (str): The new tag to associate with the metrics.
        """
        self.tag_queue.put(tag)
        logging.info("Tag change request sent: %s", tag)

    def _run_collector(self, stop_event: Event, metrics_queue: Queue, tag_queue: Queue, interval: float) -> None:
        """
        Internal method run as a separate process to collect performance metrics at regular intervals. 
        Collects metrics including CPU, network, and GPU usage, and places them into a queue for writing.

        Parameters:
        -----------
        - stop_event (Event): An event to signal when to stop the collector process.
        - metrics_queue (Queue): A queue to store collected metrics for writing.
        - tag_queue (Queue): A queue to receive tag changes.
        - interval (float): The interval in seconds between each metrics collection.
        """
        collector = ResourceMetricCollector(Device.cuda.all())
        collector.start(tag="metrics-daemon")
        current_tag: Optional[str] = None

        while not stop_event.is_set():
            # Check for tag updates
            try:
                while True:  # Process all pending tag updates
                    current_tag = tag_queue.get_nowait()
            except Empty:
                pass

            metrics = self._collect_metrics(collector, current_tag)
            metrics_queue.put(metrics)
            time.sleep(interval)

        collector.stop()

    def _run_writer(self, stop_event: Event, metrics_queue: Queue, filepath: str) -> None:
        """
        Internal method run as a separate process to write collected metrics to a CSV file. 
        This process continuously writes metrics to the specified file until a stop event is set.

        Parameters:
        -----------
        - stop_event (Event): An event to signal when to stop the writer process.
        - metrics_queue (Queue): A queue from which to retrieve collected metrics for writing.
        - filepath (str): The path to the file where metrics will be written.
        """
        first_collect = True
        while not stop_event.is_set():
            try:
                metrics = metrics_queue.get(timeout=1)
                self._write_metrics(metrics, filepath, first_collect)
                if first_collect:
                    first_collect = False
            except Empty:
                continue

    def _get_cpu_usage_per_core(self) -> Dict[str, float]:
        """
        Collects CPU usage metrics for each core.

        Returns:
        --------
        - Dict[str, float]: A dictionary where keys are core identifiers and values are the respective CPU usage percentages.
        """
        cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
        return {f"cpu_core_{i+1} (%)": percent
                for i, percent in enumerate(cpu_percent)}

    def _get_network_bandwidth(self) -> Dict[str, float]:
        """
        Collects network bandwidth usage metrics.

        Returns:
        --------
        - Dict[str, float]: A dictionary where keys are network interface names suffixed with "/sent" or "/recv" 
                            and values are the respective bandwidth in Mbps.
        """
        interfaces = psutil.net_io_counters(pernic=True)
        it = {}
        for interface, stats in interfaces.items():
            bytes_sent = stats.bytes_sent
            bytes_recv = stats.bytes_recv
            mbps_sent = bytes_sent * 8 / (1024 * 1024)
            mbps_recv = bytes_recv * 8 / (1024 * 1024)
            it[f"network_{interface}/sent (Mbps)"] = mbps_sent
            it[f"network_{interface}/recv (Mbps)"] = mbps_recv
        return it

    def _clean_column_name(self, col: str) -> str:
        """
        Cleans the column name by removing specific prefixes.

        Parameters:
        -----------
        - col (str): The column name to be cleaned.

        Returns:
        --------
        - str: The cleaned column name.
        """
        rm_prefix = ["metrics-daemon/host/", "metrics-daemon/"]
        for prefix in rm_prefix:
            if col.startswith(prefix):
                col = col[len(prefix):]
        return col

    def _collect_metrics(self, collector: ResourceMetricCollector, current_tag: Optional[str]) -> Dict[str, Union[float, str, None]]:
        """
        Collects and processes performance metrics including CPU, network, and GPU usage. 
        Optionally includes a tag to differentiate metrics.

        Parameters:
        -----------
        - collector (ResourceMetricCollector): The GPU metrics collector.
        - current_tag (Optional[str]): An optional tag to include with the metrics.

        Returns:
        --------
        - Dict[str, Union[float, str, None]]: A dictionary containing the collected metrics.
        """
        # Collect the metrics and cast it to the appropriate type
        raw_metrics = collector.collect()
        metrics = cast(Dict[str, Union[float, str, None]], raw_metrics)

        # Collect CPU and network metrics
        cpu_metrics = self._get_cpu_usage_per_core()
        metrics.update(cpu_metrics)

        network_metrics = self._get_network_bandwidth()
        metrics.update(network_metrics)

        metrics['tag'] = current_tag

        return metrics

    def _write_metrics(self, metrics: Dict[str, Union[float, str, None]], filepath: str, first_collect: bool) -> None:
        """
        Writes collected metrics to a CSV file. If it's the first time writing, a header is included.

        Parameters:
        -----------
        - metrics (Dict[str, Union[float, str, None]]): The metrics to write to the file.
        - filepath (str): The path to the file where metrics will be written.
        - first_collect (bool): Indicates whether this is the first collection (if True, writes the header).
        """
        df_metrics = pd.DataFrame.from_records([metrics])
        df_metrics.columns = [self._clean_column_name(col)
                              for col in df_metrics.columns]

        try:
            if first_collect and not os.path.isfile(filepath):
                df_metrics.to_csv(filepath, index=False)
                logging.info("First collection completed at path %s", filepath)
            else:
                if df_metrics.isnull().all().all():
                    logging.info("Skipping empty row")
                    return

                file_exists = os.path.isfile(filepath)
                with open(filepath, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=df_metrics.columns)

                    # Write the header only if the file does not exist or the header is missing
                    if not file_exists or f.tell() == 0:
                        writer.writeheader()

                    writer.writerow(df_metrics.iloc[0].to_dict())

                    if self.debug_mode:
                        logging.info("Data written to %s with duration %s",
                                     filepath, df_metrics.iloc[0].get('duration (s)', 'N/A'))
                    f.flush()
        except (IOError, OSError) as e:
            logging.error("File I/O error writing to %s: %s", filepath, str(e))
        except ValueError as e:
            logging.error("Value error during file write: %s", str(e))
