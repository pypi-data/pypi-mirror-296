# This file is part of hvspatialpy, a Python package for evaluating
# spatial variability of a site utilizing spatially distributed HVSR.

# Copyright (c) 2024 Francisco Javier Ornelas (jornela1@g.ucla.edu)

"""Functions for evaluating the spatial variability of a site."""

import os
import logging
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import rasterio
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MaxNLocator
import ipywidgets as widgets
from IPython.display import display

from .hvcorr import *

logger = logging.getLogger(__name__)

__all__ = ['update_correlations']


def _plot_intervals(ax1, freq, mean_ref, min_freq, max_freq, freq_trun=0.1):
    """

    A function to plot the frequency intervals of the reference HVSR.

    Parameters:

    freq_trun: float
        The frequency to truncate the HVSR mean curve.
    min_freq: float
        The minimum frequency in the interval.
    max_freq: float
        The maximum frequency in the interval.

    """
    ax1.clear()
    colors = ['blue', 'red', 'green']
    lines = [Line2D([0], [0], color=c, linewidth=3, linestyle='-') for c in colors]
    labels = ['HVSR ref. mean', 'Min. Freq. Interval', 'Max. Freq. Interval']
    ax1.semilogx(freq, mean_ref, color='blue')
    ax1.set_xlim(freq_trun, max(freq))
    for i in range(len(min_freq)):
        ax1.axvline(x=min_freq[i], color='r')
        ax1.axvline(x=max_freq[i], color='g')
    ax1.set_xlabel('Frequency, $f$ (Hz)')
    ax1.set_ylabel('HVSR')
    ax1.legend(lines, labels)
    plt.show()


def _update_colorbar(ax, cbar, scatter, correlation_type='lcss'):
    """
    Update the colorbar with the latest scatter plot and label.

    Parameters:
    cbar: obj
        The colorbar object to be updated.
    scatter: fig
        The new scatter plot object.
    correlation_type: str
        The type of correlation to be displayed in the colorbar label.

    """

    cax = plt.gca().inset_axes([1.02, 0, 0.03, 1])

    cax.clear()
    cbar = plt.colorbar(scatter, ax=ax, cax=cax, pad=0.02)
    cbar.set_label(f'{correlation_type.capitalize()} Correlation Value')

    plt.tight_layout()


def _plot_site_image(ax2, df_site, correlation_type='lcss', frequency_interval=None):
    """
    Plot site data on top of a topographic relief map using EPSG:4326.

    Parameters:

    df_site: Dataframe
        DataFrame containing 'longitude', 'latitude', and 'correlation_value'
    correlation_type: str
        Type of correlation value (used for colorbar label)
    frequency_interval: int
        Optional frequency interval to filter the data

    return:
        Matplotlib figure object
    """

    if df_site.empty:
        print("DataFrame is empty.")
        return

    if frequency_interval:
        df_site = df_site[df_site['freq_interval'] == frequency_interval]

    lon_plt = df_site['longitude'].values
    lat_plt = df_site['latitude'].values

    ax2.clear()

    # Under construction

    #     raster_path = r'C:\Users\Javier Ornelas\OneDrive\Documents\HVSRdata_Main\ARCgis maps\NE1_LR_LC_SR_W/NE1_LR_LC_SR_W.tif'
    #     raster_path = os.path.join(os.path.dirname(__file__, 'Data', 'NE1_LR_LC_SR_W.tif'))

    #     with rasterio.open(raster_path) as src:
    #         img = src.read(1)
    #         extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

    #     ax2.imshow(img, cmap='viridis', extent=extent, alpha=0.5, origin='upper', aspect='auto')

    scatter = ax2.scatter(
        lon_plt,
        lat_plt,
        c=df_site['correlation_value'],
        s=100,
        cmap='plasma',
        edgecolor='k',
        alpha=0.7)

    cbar = None

    _update_colorbar(ax=ax2, cbar=cbar, scatter=scatter, correlation_type=correlation_type)

    ax2.set_aspect('auto')

    ax2.set_xlabel('Longitude', fontsize=14)
    ax2.set_ylabel('Latitude', fontsize=14)

    ax2.set_xlim([lon_plt.min() - 0.002, lon_plt.max() + 0.002])
    ax2.set_ylim([lat_plt.min() - 0.002, lat_plt.max() + 0.002])

    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax2.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.4f}'))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.4f}'))

    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    plt.setp(ax2.get_yticklabels(), rotation=45, ha='right', fontsize=10)

    ax2.grid(True, linestyle='--', alpha=0.7)

    plt.show()

    plt.tight_layout()


def _update_dataframe(base_dir, site, num_peaks, min_freq, max_freq):
    """
    Function to update the frequency interval dataframe

    Parameters:

    base_dir: str
        Base directory path where the site and test files are stored.
    site: int
        Site test number
    num_peaks: int
        Number of peaks within the HVSR curve.
    min_freq: float
        Minimum frequency of the interval
    max_freq: float
        Maximum frequency of the interval

    return:
        Updated dataframe of the frequency intervals.
    """
    test_list = []
    site_list = []
    freq_min_list = []
    freq_max_list = []
    num_peaks_list = []

    site_dir_path = os.path.join(base_dir, site)
    for test in os.listdir(site_dir_path):
        test_dir_path = os.path.join(site_dir_path, test)

        if not os.path.isdir(test_dir_path) or test.endswith('.csv') or test == 'Mean Curves':
            continue

        for i, (min_f, max_f) in enumerate(zip(min_freq, max_freq)):
            test_list.append(test)
            site_list.append(site)
            freq_min_list.append(min_f)
            freq_max_list.append(max_f)
            num_peaks_list.append(num_peaks)

    freq_df = pd.DataFrame({
        'site': site_list,
        'tests': test_list,
        'numPeaks': num_peaks_list
    })

    for i in range(len(min_freq)):
        min_vals = []
        max_vals = []

        for j in range(len(test_list)):
            min_vals.append(min_freq[i])
            max_vals.append(max_freq[i])

        freq_df[f'freq_int_{i}_min'] = min_vals
        freq_df[f'freq_int_{i}_max'] = max_vals

    return freq_df


def update_correlations(base_dir, site, xml_folder_name, unique_folder_name, ref_test_name, mean_file_name,
                        unique_flag=True, auto_dist_calc_flag=True, freq_trun=0.1, dist_meas_df=None,
                        loc_df_manual=None, correlation_type='lcss', frequency_interval=None, threshold=1.6,
                        min_distance=1, global_constraint='sakoe_chiba', eps=0.75, sakoe_chiba_radius=10,
                        dist_range_list=None):
    """
    Function to update the correlation plot when different input parameters change.

    Parameters:

    dist_range_list: str
        String of tuple list to evaluate different distance ranges that were used in the study.
    sakoe_chiba_radius: int
        Radius of warping window to allow a horizontal shift between different points in a curve. Note: only for 'lcss'
        and 'dtw'.
    eps: float
        Matching threshold used in 'lcss' correlation. Note: only for 'lcss'.
    global_constraint: str
        String indicating whether to use sakoe_chiba radius or itakura slope. Note: only for 'lcss' and 'dtw'.
    loc_df_manual: str
        Path where the location dataframe (.csv) is stored, showing the true locations of the test points. Note: only use
        if the auto flag is not working.
    dist_meas_df: str
        Path where the distance measured dataframe (.csv) is stored, showing the distances from the reference. Note:
        only use if the auto flag is not working.
    auto_dist_calc_flag: boolean
        Indicated whether to use .xml files to identify locations of test points or use a .csv file (False).
    unique_flag: boolean
        Indicates if the folder scheme is unique, meaning that more folders would need to be used to do computation.
        Use unique_folder_name if this is true.
    mean_file_name: str
        Indicates the filename used for the mean HVSR curve.
    ref_test_name: str
        Indicates the name of the reference test.
    unique_folder_name: str
        Indicates the unique path where files are stored.
    freq_df: dataframe
        The dataframe where the frequency interval information is stored.
    base_dir: str
        Indicates the base directory where all the tests are stored.
    site: str
        Indicates the site name where the tests for that site are stored.
    xml_folder_name: str
        Indicates the folder name where the xml files are relative to site and tests.
    correlation_type: str
        Indicates the type of correlation used in the analysis.

    return:
        The frequency, correlation dataframes and the figure used in the analysis.
    """
    if unique_flag:
        ref_file_path = os.path.join(base_dir, site, ref_test_name, unique_folder_name, mean_file_name)
    else:
        ref_file_path = os.path.join(base_dir, site, ref_test_name, mean_file_name)

    ref = pd.read_csv(ref_file_path, header=None)

    try:
        ref = ref[1:].astype(float)
    except ValueError as e:
        raise ValueError(f"DataFrame conversion error: {e}")

    ref = ref[ref[0] > freq_trun]

    mean_ref = ref[1].values
    freq = ref[0].values

    left_troughs, right_troughs, peaks, troughs = _find_nearest_trough(y=mean_ref,
                                                                       threshold=threshold, min_distance=min_distance)
    min_freq_idx = np.asarray(left_troughs)
    max_freq_idx = np.asarray(right_troughs)

    num_peaks = len(min_freq_idx)

    min_freq = [freq[i] for i in min_freq_idx]
    max_freq = [freq[i] for i in max_freq_idx]

    fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(10, 5))

    fig.suptitle(f'Analysis for Site - {site}')

    _plot_intervals(ax1=ax1, freq=freq, mean_ref=mean_ref, min_freq=min_freq, max_freq=max_freq, freq_trun=freq_trun)

    def on_change(_):
        updated_min_freq = [text_min[i].value for i in range(len(min_freq))]
        updated_max_freq = [text_max[i].value for i in range(len(max_freq))]
        _plot_intervals(ax1=ax1, freq=freq, mean_ref=mean_ref, min_freq=updated_min_freq,
                        max_freq=updated_max_freq, freq_trun=freq_trun)
        df = _update_dataframe(base_dir=base_dir, site=site, num_peaks=num_peaks,
                               min_freq=updated_min_freq, max_freq=updated_max_freq)
        df_all = compute_correlations(base_dir=base_dir, site=site, freq_df=df,
                                      xml_folder_name=xml_folder_name, unique_folder_name=unique_folder_name,
                                      ref_test_name=ref_test_name, mean_file_name=mean_file_name,
                                      unique_flag=unique_flag, auto_dist_calc_flag=auto_dist_calc_flag,
                                      correlation_type=correlation_type, dist_meas_df=dist_meas_df,
                                      loc_df_manual=loc_df_manual, global_constraint=global_constraint,
                                      eps=eps, sakoe_chiba_radius=sakoe_chiba_radius,
                                      dist_range_list=dist_range_list)
        _plot_site_image(ax2=ax2, df_site=df_all, correlation_type=correlation_type,
                         frequency_interval=frequency_interval)

    text_min = [widgets.FloatText(value=str(np.round(val, 4)), description=f'Min FI Int. {i}') for i, val in
                enumerate(min_freq)]
    text_max = [widgets.FloatText(value=str(np.round(val, 4)), description=f'Max FI Int. {i}') for i, val in
                enumerate(max_freq)]

    for text in text_min + text_max:
        text.observe(on_change, names=['value'])

    box_layout_1 = widgets.HBox([*text_min])
    box_layout_2 = widgets.HBox([*text_max])

    display(box_layout_1)
    display(box_layout_2)

    df = _update_dataframe(base_dir=base_dir, site=site, num_peaks=num_peaks, min_freq=min_freq, max_freq=max_freq)

    df_all = compute_correlations(base_dir=base_dir, site=site, freq_df=df, xml_folder_name=xml_folder_name,
                                  unique_folder_name=unique_folder_name,
                                  ref_test_name=ref_test_name, mean_file_name=mean_file_name, unique_flag=unique_flag,
                                  auto_dist_calc_flag=auto_dist_calc_flag, correlation_type=correlation_type,
                                  dist_meas_df=dist_meas_df,
                                  loc_df_manual=loc_df_manual, global_constraint=global_constraint,
                                  eps=eps, sakoe_chiba_radius=sakoe_chiba_radius, dist_range_list=dist_range_list)

    _plot_site_image(ax2=ax2, df_site=df_all, correlation_type=correlation_type, frequency_interval=frequency_interval)

    plt.tight_layout()

    return df, df_all, fig
